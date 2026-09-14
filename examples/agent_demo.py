import asyncio
import sys
from typing import Any

from agents import Agent, Runner, RunContextWrapper
from agents.mcp import MCPServerStdio

from mcp_rescue.classifier import rescue_error
from mcp_rescue.models import ToolInfo


TOOL_INFO = {
    "booking": ToolInfo(
        name="booking",
        read_only=False,
        idempotent=False,
        destructive=False,
    ),
    "weather_timeout": ToolInfo(
        name="weather_timeout",
        read_only=True,
        idempotent=True,
        destructive=False,
    ),
    "send_email_timeout": ToolInfo(
        name="send_email_timeout",
        read_only=False,
        idempotent=False,
        destructive=False,
    ),
}


def rescue_failure(
    context: RunContextWrapper[Any],
    error: Exception,
) -> str:

    tool_name = getattr(context, "tool_name", "unknown")
    tool = TOOL_INFO.get(tool_name)

    rescued = rescue_error(
        str(error),
        tool,
    )

    print("\n[MCP-Rescue]")
    print("Tool:", tool_name)
    print("Category:", rescued.category)
    print("Action:", rescued.action)
    print("Retryable:", rescued.retryable)
    print("Message:", rescued.message)

    return (
        "MCP-Rescue recovery report:\n"
        f"tool={tool_name}\n"
        f"category={rescued.category.value}\n"
        f"action={rescued.action.value}\n"
        f"retryable={rescued.retryable}\n"
        f"error={rescued.message}\n\n"
        "Follow the recovery action exactly. "
        "If action=ask_user, do not retry the tool. "
        "Ask the user for the information needed to continue. "
        "Never claim that the tool succeeded."
    )


async def main():

    async with MCPServerStdio(
        name="mcp-rescue-demo",
        params={
            "command": sys.executable,
            "args": ["examples/failing_server.py"],
        },
        failure_error_function=rescue_failure,
        max_retry_attempts=0,
    ) as server:

        agent = Agent(
            name="MCP Rescue Demo Agent",
            model="gpt-3.5-turbo",
            instructions=(
                "You are testing MCP-Rescue. "
                "When explicitly asked to call a tool, actually call it. "
                "When a tool fails and returns an MCP-Rescue recovery report, "
                "follow its recovery action. "
                "Do not claim a failed tool call succeeded."
            ),
            mcp_servers=[server],
        )

        result = await Runner.run(
            agent,
            (
                "Call the booking tool exactly once with "
                "date='2026-01-01'. "
                "Then follow the recovery instruction."
            ),
        )

        print("\nAgent final output:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())