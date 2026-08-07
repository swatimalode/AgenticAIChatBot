from openai import OpenAI
from config import BASE_URL, API_KEY, MODEL
from tool_schemas import tools
import json
import tool_registry

messages = [
    {"role": "system", "content": "You are a helpful AI assistant. Use tools only when external information or actions are required. You can always reason, summarize, rewrite, explain, analyze, compare, and answer questions using the information already available in the conversation. Use tools only for actions when tools are available for those actions. If a task requires both reasoning and tools, first use the appropriate tool, then perform the reasoning yourself, then call another tool if needed."}
]

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

while True:
    user_imput = input("User: ")

    if user_imput.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_imput})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )
    message = response.choices[0].message

   # Did the model request a tool?
    while message.tool_calls:

        tool_call = message.tool_calls[0]

        print("Tool Name:", tool_call.function.name)
        print("Arguments:", tool_call.function.arguments)

        arguments = json.loads(tool_call.function.arguments)
        print("Parsed Arguments:", arguments)

        # Execute Python function
        tool_name = tool_call.function.name

        function = tool_registry.tool_registry[tool_name]

        result = function(**arguments)

        print("Tool Result:", result)

        # Add assistant's tool request
        messages.append(message)

        # Add tool result
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        # Second API call
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message

    
    assistant_response = message.content
    messages.append({"role": "assistant", "content": assistant_response})

    print(f"Assistant: {assistant_response}")

print("Exiting the chat. Goodbye!")
print("------------------------------------------------")
print("Recent messages:")
print(messages)
print("------------------------------------------------")