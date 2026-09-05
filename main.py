from openai import OpenAI
from config import BASE_URL, API_KEY, MODEL, MAX_MESSAGES, SUMMERIZE_BATCH
import json
from tool_schemas import tools
import tool_registry
from memory.memory_manager import MemoryManager
from utils.prompt import system_prompt

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel


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
# Request model
# -----------------------------

class ChatRequest(BaseModel):
    message: str


# -----------------------------
# Your existing chatbot logic
# -----------------------------

def chat(user):

    memory.add_short_term({
        "role": "user",
        "content": user
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
def chat_endpoint(request: ChatRequest):

    return StreamingResponse(
        chat(request.message),
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
                font-family: Arial;
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

            input {
                width: 75%;
                padding: 12px;
                font-size: 16px;
            }

            button {
                padding: 12px 20px;
                font-size: 16px;
            }

        </style>

    </head>


    <body>

        <h1>🤖 Welcome To Swati's AI Chatbot</h1>

        <div id="chat"></div>

        <input
            id="message"
            type="text"
            placeholder="Type your message..."
        />

        <button onclick="sendMessage()">
            Send
        </button>


        <script>

            async function sendMessage() {

                const input = document.getElementById("message");

                const message = input.value.trim();

                if (!message) {
                    return;
                }

                const chat = document.getElementById("chat");

                chat.innerHTML +=
                    `<div class="user">You: ${message}</div>`;

                const assistantDiv = document.createElement("div");

                assistantDiv.className = "assistant";

                assistantDiv.innerHTML = "Assistant: ";

                chat.appendChild(assistantDiv);

                input.value = "";

                const response = await fetch("/chat", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })

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

                    assistantDiv.innerHTML =
                        "Assistant: " + marked.parse(assistantText);

                    chat.scrollTop = chat.scrollHeight;
                }
            }

            const input = document.getElementById("message");

            input.addEventListener("keydown", function(event) {

                if (event.key === "Enter") {
                    event.preventDefault();
                    sendMessage();
                }

            });

        </script>

    </body>

    </html>
    """