from openai import OpenAI
from config import BASE_URL, API_KEY, MODEL
import json
from tool_schemas import tools
import tool_registry

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

messages = [
    {"role": "system", "content": """You are a helpful AI assistant.
You have access to tools.
Rules:
1. Whenever a user's request requires information that can be obtained using a tool, ALWAYS use the appropriate tool.
2. Never ask the user for information that one of your tools can obtain.
3. If multiple tools are required, call them one after another until you have everything needed to answer.
4. After receiving a tool result, continue reasoning before deciding whether another tool is needed.
5. Do not mention which tools you are using unless the user asks.
6. Give the final answer only after all required tools have been executed.
7. Use your own reasoning for summarizing, explaining, comparing, rewriting, and analysis. Use tools only when external data or actions are needed."""}
]

while True:

    user = input("\nUser: ")

    if user == "exit":
        break

    messages.append({
        "role":"user",
        "content": user
    })

    print("\nAssistant: ", end="", flush=True)

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            stream=True
        )

        assistant_txt=""
        tool_calls = {}

        for chunk in response:

            finished_reason = chunk.choices[0].finish_reason
            delta = chunk.choices[0].delta

            if delta.content:
                assistant_txt += delta.content
                print(delta.content, end="", flush=True)

            if delta.tool_calls:
                for tool_call in delta.tool_calls:
                    index = tool_call.index

                    if index not in tool_calls:
                        tool_calls[index] = {
                            "id":"",
                            "type": "function",
                            "function":{
                                "name":"",
                                "arguments":""
                            }
                        }

                    if tool_call.id:
                        tool_calls[index]["id"] = tool_call.id

                    if tool_call.function.name:
                        tool_calls[index]["function"]["name"] = tool_call.function.name

                    if tool_call.function.arguments:
                        tool_calls[index]["function"]["arguments"] = tool_call.function.arguments

        if finished_reason == "stop":
            messages.append({
                "role":"assistant",
                "content": assistant_txt
            })
            break

        if finished_reason == "tool_calls":
            for key in tool_calls.keys():
                arguments = json.loads(tool_calls[key]["function"]["arguments"])
                function = tool_registry.tool_registry[tool_calls[key]["function"]["name"]]
                result = function(**arguments)

                messages.append({
                    "role":"assistant",
                    "content":"",
                    "tool_calls":[tool_calls[key]]
                })

                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_calls[key]["id"],
                    "content": str(result)
                })
            continue

print("\n------------------History ----------------\n",
      messages,
      "\n------------------ End -------------------\n")

print("\n ---------------------------------------")
print("\n          Good Bye !!!                  ")
print("\n ---------------------------------------")