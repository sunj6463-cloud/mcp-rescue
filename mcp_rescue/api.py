from mcp.types import CallToolResult

from mcp_rescue.adapters.mcp import parse_mcp_result
from mcp_rescue.classifier import rescue_error
from mcp_rescue.models import RescueError, ToolInfo


def rescue_mcp_result(
    result: CallToolResult,
    tool: ToolInfo | None = None,
) -> RescueError:
    raw = parse_mcp_result(result)

    return rescue_error(
        raw,
        tool,
    )