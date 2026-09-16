import asyncio
import json
import os
import sys

from openai import OpenAI
from mcp import Client, StdioServerParameters

from mcp_rescue.adapters.mcp import parse_mcp_result
from mcp_rescue.classifier import rescue_error
from mcp_rescue.models import ToolInfo
from mcp_rescue.runtime import allow_automatic_retry

# =========================
# Qwen API
# =========================

qwen = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    timeout=20.0,
)


# =========================
# Tell Qwen what tools exist
# =========================

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


# =========================
# Tool safety metadata
# =========================

TOOL_INFO = {
    "booking": ToolInfo(
        name="booking",
        read_only=False,
        idempotent=False,
        destructive=False,
    )
}


async def main():

    # -------------------------
    # 1. User message
    # -------------------------

    messages = [
        {
            "role": "user",
            "content": "请帮我预订 2026-01-01，请使用 booking 工具。",
        }
    ]

    # -------------------------
    # 2. First Qwen request
    # Qwen decides whether to call a tool
    # -------------------------

    response = qwen.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message

    # Qwen may decide not to call a tool
    if not message.tool_calls:
        print("Qwen did not call any tool.")
        print("Response:", message.content)
        return

    # For this demo we only process the first tool call
    tool_call = message.tool_calls[0]

    tool_name = tool_call.function.name
    arguments = json.loads(
        tool_call.function.arguments
    )

    print("Qwen wants to call:")
    print("tool:", tool_name)
    print("arguments:", arguments)

    # -------------------------
    # 3. Start MCP server
    # -------------------------

    server = StdioServerParameters(
        command=sys.executable,
        args=["examples/failing_server.py"],
    )

    async with Client(server) as mcp_client:

        # -------------------------
        # 4. Actually execute MCP tool
        # -------------------------

        result = await mcp_client.call_tool(
            tool_name,
            arguments,
        )

        print("\nMCP result:")
        print(result)

        # -------------------------
        # 5. Add Qwen's tool-call message
        # to conversation history
        # -------------------------

        messages.append(
            message.model_dump(exclude_none=True)
        )

        # =========================
        # Tool succeeded
        # =========================

        if not result.is_error:

            tool_result_text = ""

            for item in result.content:
                if item.type == "text":
                    tool_result_text += item.text

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result_text,
                }
            )

        # =========================
        # Tool failed
        # =========================

        else:

            # -------------------------
            # 6. MCP result -> RawError
            # -------------------------

            raw = parse_mcp_result(result)

            # Get safety metadata
            tool_info = TOOL_INFO.get(tool_name)

            # -------------------------
            # 7. MCP-Rescue
            # -------------------------

            rescued = rescue_error(
                raw,
                tool_info,
            )

            automatic_retry_allowed = allow_automatic_retry(rescued)

            print(
                "Automatic retry allowed:",
                automatic_retry_allowed,
            )
            
            print("\nMCP-Rescue:")
            print("Category:", rescued.category)
            print("Action:", rescued.action)
            print("Retryable:", rescued.retryable)
            print("Message:", rescued.message)

            # -------------------------
            # 8. Build structured recovery report
            # for the LLM
            # -------------------------

            recovery_report = (
                "MCP-Rescue recovery report:\n"
                f"tool={tool_name}\n"
                f"category={rescued.category.value}\n"
                f"action={rescued.action.value}\n"
                f"retryable={rescued.retryable}\n"
                f"error={rescued.message}\n\n"
                "Follow the recovery action exactly. "
                "If action=ask_user, do not retry the tool. "
                "Ask the user for the missing or corrected information. "
                "Never claim that the tool succeeded."
            )

            # -------------------------
            # 9. Tell Qwen the result of
            # its previous tool call
            # -------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": recovery_report,
                }
            )

        # -------------------------
        # 10. Second Qwen request
        # Qwen sees tool result / recovery result
        # -------------------------

        final_response = qwen.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        final_message = final_response.choices[0].message

        print("\nQwen final response:")
        print(final_message.content)

        if final_message.tool_calls:
            if not automatic_retry_allowed:
                print("\n[Runtime]")
                print("Blocked automatic tool retry.")

                for call in final_message.tool_calls:
                    print(
                        "Blocked:",
                        call.function.name,
                        call.function.arguments,
                    )

                return

            # 只有允许自动 retry 时，才可能继续执行
            for call in final_message.tool_calls:
                print(
                    "\nAutomatic retry allowed for:",
                    call.function.name,
                    call.function.arguments,
                )


if __name__ == "__main__":
    asyncio.run(main())