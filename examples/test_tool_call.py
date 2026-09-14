import os
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    timeout=20.0,
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "booking",
            "description": "Book something for a specified date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Booking date in YYYY-MM-DD format",
                    }
                },
                "required": ["date"],
            },
        },
    }
]


response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {
            "role": "user",
            "content": "请帮我预订 2026-01-01，请使用 booking 工具。",
        }
    ],
    tools=tools,
    tool_choice="auto",
)


message = response.choices[0].message

print("content:", message.content)
print("tool_calls:", message.tool_calls)


if message.tool_calls:
    for tool_call in message.tool_calls:
        print("\nAI wants to call:")
        print("tool name:", tool_call.function.name)
        print("arguments:", tool_call.function.arguments)