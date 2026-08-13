from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL
from utils.prompt import summerize_prompt

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

def summerize(messages):
    prompt = summerize_prompt
    for message in messages:
        prompt += (
            f"\nrole: {message['role']}, "
            f"content: {message['content']}"
        )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content