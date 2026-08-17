import json
from openai import OpenAI
#from config import BASE_URL, API_KEY, MODEL

client = OpenAI(
    base_url="http://localhost:11434/v1", 
    api_key="ollama"
)

def verify_tool_result(tool_name, user_question, tool_result):
    prompt = f""" 
        You are a tool-result verifier.

        User question:
        {user_question}

        Tool used:
        {tool_name}

        Tool result:
        {tool_result}

        Determine whether the tool result provides sufficient and relevant
        evidence to answer the user's question.

        Return ONLY valid JSON:

        {{
            "verified": true,
            "reason": "short explanation"
        }}

        or

        {{
            "verified": false,
            "reason": "short explanation"
        }}

        Rules:
        - Do not use your own knowledge.
        - Judge only whether the tool result supports the answer.
        - If the result is irrelevant, incomplete, contradictory, or ambiguous,
        return verified=false.
        - If the result clearly contains the information needed to answer,
        return verified=true.
    """

    response = client.chat.completions.create(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": "You verify tool results."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )
    content = response.choices[0].message.content

    return json.loads(content)

result = verify_tool_result(
    user_question="Who won IPL 2025?",
    tool_name="search",
    tool_result=[
        {
            "title": "IPL Winners List",
            "snippet": "Royal Challengers Bengaluru won IPL 2025."
        }
    ]
)

print(result)