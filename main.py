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
7. Use your own reasoning for summarizing, explaining, comparing, rewriting, and analysis. Use tools only when external data or actions are needed.
8. When a search tool returns structured data such as JSON, use the information inside the results to answer the user's question naturally. 
Do not simply repeat or dump the raw search results unless the user specifically asks for them.
9. You have a search tool that provides access to current internet information.
10. ALWAYS use the search tool when the user asks about current events, latest news, recent information, current facts, or information that may
have changed after your knowledge cutoff.
11. Do not claim that you cannot access the internet when the search tool is available.
12. If search results are insufficient or unclear, perform another search with a more specific query rather than guessing.
13. Never invent facts when the search results do not provide enough evidence. Clearly say when reliable information could not be found.
14. After receiving search results, use their content to formulate a natural answer. Do not dump raw JSON unless the user asks for it.
15. If a question asks for current, recent, latest, upcoming, or historical information that may be verified online, you MUST call the search tool before answering.
16. Do not use your own knowledge to determine whether an event has happened. The search results must determine that.
17. When using the search tool, evaluate the quality of the search results before answering.
18. Do not treat a single weak source, social-media result, video, or unclear snippet as sufficient evidence for an important factual claim.
19. For factual questions, prefer multiple independent and credible sources.
20. If the search results are weak, irrelevant, contradictory, or do not directly answer the question, call the search tool again with a more specific query.
21. When searching for a specific fact, include the exact entity, year, event, and fact being requested in the search query.
22. Do not say that information is unavailable simply because the first search results were poor. Try another search first.
23. When reliable search results clearly establish an answer, answer directly and confidently."""}
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
                        tool_calls[index]["function"]["arguments"] += tool_call.function.arguments

        if finished_reason == "stop":
            messages.append({
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