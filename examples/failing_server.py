from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("mcp-rescue-demo")


@mcp.tool()
def rate_limited() -> str:
    raise ToolError("429 Too Many Requests")


@mcp.tool()
def booking(date: str) -> str:
    if date == "2026-01-01":
        raise ToolError("Booking date must be in the future")
    return f"Booked for {date}"

@mcp.tool()
def weather_timeout() -> str:
    raise ToolError("connection timeout")


@mcp.tool()
def send_email_timeout() -> str:
    raise ToolError("connection timeout")


if __name__ == "__main__":
    mcp.run()