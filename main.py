from openai import OpenAI
from config import BASE_URL, API_KEY, MODEL, MAX_MESSAGES, SUMMERIZE_BATCH
import json
from tool_schemas import tools
import tool_registry
from memory.memory_manager import MemoryManager
from utils.prompt import system_prompt
from utils.chunker import store
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, StreamingResponse
# from pydantic import BaseModel


client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

memory = MemoryManager(
    MAX_MESSAGES,
    SUMMERIZE_BATCH
)

app = FastAPI()

# -----------------------------
# Your existing chatbot logic
# -----------------------------

def chat(message, file):

    memory.add_short_term({
            "role": "user",
            "content": message
        })

    if(file):
        upload_status = store(file)
        memory.add_short_term({
                "role": "system",
                "content": upload_status
            })

    while True:

        messages = [system_prompt] + memory.get_short_term()

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            stream=True
        )

        assistant_txt = ""
        tool_calls = {}

        for chunk in response:

            finished_reason = chunk.choices[0].finish_reason
            delta = chunk.choices[0].delta

            if delta.content:
                assistant_txt += delta.content
                yield delta.content 

            if delta.tool_calls:

                for tool_call in delta.tool_calls:

                    index = tool_call.index

                    if index not in tool_calls:

                        tool_calls[index] = {
                            "id": "",
                            "type": "function",
                            "function": {
                                "name": "",
                                "arguments": ""
                            }
                        }

                    if tool_call.id:
                        tool_calls[index]["id"] = tool_call.id

                    if tool_call.function.name:
                        tool_calls[index]["function"]["name"] = (
                            tool_call.function.name
                        )

                    if tool_call.function.arguments:
                        tool_calls[index]["function"]["arguments"] += (
                            tool_call.function.arguments
                        )

        # -----------------------------
        # Normal assistant response
        # -----------------------------

        if finished_reason == "stop":

            memory.add_short_term({
                "role": "assistant",
                "content": assistant_txt
            })

            return

        # -----------------------------
        # Tool calls
        # -----------------------------

        if finished_reason == "tool_calls":

            for key in tool_calls.keys():

                arguments = json.loads(
                    tool_calls[key]["function"]["arguments"]
                )

                function = tool_registry.tool_registry[
                    tool_calls[key]["function"]["name"]
                ]

                result = function(**arguments)

                memory.add_short_term({
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [tool_calls[key]]
                })

                memory.add_short_term({
                    "role": "tool",
                    "tool_call_id": tool_calls[key]["id"],
                    "content": str(result)
                })

            continue


# -----------------------------
# Chat endpoint
# -----------------------------

@app.post("/chat")
def chat_endpoint(message: str = Form(""), file: UploadFile | None = File(None)):

    # return file

    return StreamingResponse(
        chat(message, file),
        media_type="text/plain"
    )


# -----------------------------
# Health check
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -----------------------------
# Simple browser UI
# -----------------------------

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Swati's AI Chatbot</title>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
            }

            #chat {
                border: 1px solid #ddd;
                padding: 20px;
                height: 500px;
                overflow-y: auto;
                margin-bottom: 20px;
            }

            .user {
                margin: 10px 0;
                font-weight: bold;
            }

            .assistant {
                margin: 10px 0 20px 0;
            }

            .input-container {
                display: flex;
                align-items: center;
                width: 100%;
                height: 65px;
                background: white;
                border: 1px solid #444;
                border-radius: 35px;
                padding: 0 10px;
                box-sizing: border-box;
                gap: 8px; /* Added gap to prevent elements from crashing into each other */
            }

            .attach-button {
                width: 45px;
                height: 45px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 32px;
                color: black;
                cursor: pointer;
                border-radius: 50%;
                flex-shrink: 0;
            }

            .attach-button:hover {
                background: #eee; /* Changed to light gray so black text remains visible */
            }

            #message {
                flex: 1;
                height: 100%;
                border: none;
                outline: none;
                background: transparent;
                color: black;
                font-size: 18px;
                padding: 0 15px;
            }

            #message::placeholder {
                color: #aaa;
            }

            /* Styled File Preview Chip */
            .file-preview-chip {
                display: flex;
                align-items: center;
                gap: 6px;
                background-color: #f1f3f4;
                border-radius: 16px;
                padding: 6px 12px;
                font-size: 14px;
                color: #3c4043;
                max-width: 180px;
                flex-shrink: 0;
            }

            .file-preview-chip span {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .file-preview-chip button {
                background: none;
                border: none;
                color: #5f6368;
                cursor: pointer;
                font-size: 16px;
                padding: 0;
                line-height: 1;
            }

            .file-preview-chip button:hover {
                color: #000;
            }

            .send-button {
                width: 50px;
                height: 50px;
                border: none;
                border-radius: 50%;
                background: blue;
                color: white;
                font-size: 24px;
                cursor: pointer;
                flex-shrink: 0;
            }

            .send-button:hover {
                background: #3875e8;
            }
        </style>
    </head>

    <body>

        <h1>🤖 Welcome To Swati's AI Chatbot</h1>

        <div id="chat"></div>

        <div class="input-container">

            <label for="fileInput" class="attach-button">
                +
            </label>
            <input type="file" id="fileInput" hidden>

            <input
                id="message"
                type="text"
                placeholder="Ask anything"
            />

            <!-- Dynamic file status element -->
            <div id="filePreview" class="file-preview-chip" style="display: none;">
                <span id="fileName"></span>
                <button id="removeFile" type="button" onclick="clearFile()">×</button>
            </div>

            <button onclick="sendMessage()" class="send-button">
                ➤
            </button>

        </div>

        <script>
            const fileInput = document.getElementById("fileInput");
            const filePreview = document.getElementById("filePreview");
            const fileNameSpan = document.getElementById("fileName");
            const messageInput = document.getElementById("message");
            const chat = document.getElementById("chat");

            // 1. Listen for file selection changes
            fileInput.addEventListener("change", function() {
                if (this.files && this.files.length > 0) {
                    fileNameSpan.textContent = this.files[0].name;
                    filePreview.style.display = "flex"; // Show chip
                }
            });

            // 2. Clear out the selected file when the '×' button is clicked
            function clearFile() {
                fileInput.value = "";
                filePreview.style.display = "none"; // Hide chip
                fileNameSpan.textContent = "";
            }

            async function sendMessage() {
                const message = messageInput.value.trim();
                const file = fileInput.files[0];

                // Don't send if both are empty
                if (!message && !file) {
                    return;
                }

                // Create FormData
                const formData = new FormData();
                formData.append("message", message);
                if (file) {
                    formData.append("file", file);
                }

                // Show user's message
                if (message) {
                    chat.innerHTML += `<div class="user">You: ${message}</div>`;
                }

                // Show uploaded file
                if (file) {
                    chat.innerHTML += `<div class="user">📎 File: ${file.name}</div>`;
                }

                const assistantDiv = document.createElement("div");
                assistantDiv.className = "assistant";
                assistantDiv.innerHTML = "Assistant: ";
                chat.appendChild(assistantDiv);

                // Clear inputs and reset file preview layout
                messageInput.value = "";
                clearFile();

                chat.scrollTop = chat.scrollHeight;

                // Send message + file together
                const response = await fetch("/chat", {
                    method: "POST",
                    body: formData
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let assistantText = "";

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) {
                        break;
                    }

                    const chunk = decoder.decode(value, { stream: true });
                    assistantText += chunk;

                    assistantDiv.innerHTML = "Assistant: " + marked.parse(assistantText);
                    chat.scrollTop = chat.scrollHeight;
                }
            }

            messageInput.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    event.preventDefault();
                    sendMessage();
                }
            });
        </script>

    </body>
    </html>
    """