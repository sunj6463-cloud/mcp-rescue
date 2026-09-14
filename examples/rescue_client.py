import asyncio
import sys
from mcp_rescue.adapters.mcp import parse_mcp_result
from mcp import Client, StdioServerParameters
from mcp_rescue.classifier import rescue_error
from mcp_rescue.models import ToolInfo

async def main():
    server = StdioServerParameters(
        command=sys.executable,
        args=["examples/failing_server.py"],
    )
    # tool = ToolInfo(
    #     name="rate_limited",
    #     read_only=True,
    #     idempotent=True,
    #     destructive=False,
    # )
    # async with Client(server) as client:
    #     result = await client.call_tool(
    #         "rate_limited",
    #         {},
    #     )
    #     raw = parse_mcp_result(result)
    #     print(raw)
    #     # print(result)
    #     print("raw type:", type(raw))
    #     rescued = rescue_error(raw, tool)

    #     print("rescued type:", type(rescued))
    #     print("Category:", rescued.category)
    #     print("Action:", rescued.action)
    #     print("Retryable:", rescued.retryable)
    #     print("Message:", rescued.message)
    # tool = ToolInfo(
    #     name="booking",
    #     read_only=False,
    #     idempotent=False,
    #     destructive=False,
    # )
    # async with Client(server) as client:
    #     result = await client.call_tool(
    #         "booking",
    #         {"date": "2026-01-01",},
    #     )
    #     raw = parse_mcp_result(result)
    #     print(raw)
    #     # print(result)
    #     print("raw type:", type(raw))
    #     rescued = rescue_error(raw, tool)

    #     print("rescued type:", type(rescued))
    #     print("Category:", rescued.category)
    #     print("Action:", rescued.action)
    #     print("Retryable:", rescued.retryable)
    #     print("Message:", rescued.message)

    # tool = ToolInfo(
    #     name="send_email_timeout",
    #     read_only=False,
    #     idempotent=False,
    #     destructive=False,
    # )
    tool = ToolInfo(
        name="weather_timeout",
        read_only=True,
        idempotent=True,
        destructive=False,
    )
    
    async with Client(server) as client:
        result = await client.call_tool(
            "weather_timeout",
            {},
        )
        raw = parse_mcp_result(result)
        print(raw)
        # print(result)
        print("raw type:", type(raw))
        rescued = rescue_error(raw, tool)

        print("rescued type:", type(rescued))
        print("Category:", rescued.category)
        print("Action:", rescued.action)
        print("Retryable:", rescued.retryable)
        print("Message:", rescued.message)


if __name__ == "__main__":
    asyncio.run(main())