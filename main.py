from openai import OpenAI
from config import BASE_URL, API_KEY, MODEL, MAX_MESSAGES
import json
from tool_schemas import tools
import tool_registry
from memory.short_term_memory import shortTermMemory
from utils.prompt import system_prompt

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

memory = shortTermMemory(max_message=MAX_MESSAGES)

messages = [system_prompt]

messages.extend(memory.get_messages())

while True:

    user = input("\nUser: ")

    if user == "exit":
        break
    
    memory.add({
        "role":"user",
        "content": user
    })

    print("\nAssistant: ", end="", flush=True)

    while True:

        messages = [system_prompt] + memory.get_messages()

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
                        tool_calls[index]["function"]["arguments"] += tool_call.function.arguments

        if finished_reason == "stop":
            memory.add({
                "role":"assistant",
                "content": assistant_txt
            })
            break

        if finished_reason == "tool_calls":
            for key in tool_calls.keys():
                print(tool_call)
                arguments = json.loads(tool_calls[key]["function"]["arguments"])
                function = tool_registry.tool_registry[tool_calls[key]["function"]["name"]]
                result = function(**arguments)

                print("Tool Name:------------- ", [tool_calls[key]["function"]["name"]])

                memory.add({
                    "role":"assistant",
                    "content":"",
                    "tool_calls":[tool_calls[key]]
                })

                memory.add({
                    "role":"tool",
                    "tool_call_id":tool_calls[key]["id"],
                    "content": str(result)
                })
            continue

print("\n------------------History ----------------\n",
      messages,
      "\n------------------ End -------------------\n",
      "\n\n\n ---------------------------------------", memory.get_messages())

print("\n ---------------------------------------")
print("\n          Good Bye !!!                  ")
print("\n ---------------------------------------")