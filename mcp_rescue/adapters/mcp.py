from mcp.types import CallToolResult
from mcp_rescue.models import RawError

def parse_mcp_result(result:CallToolResult) -> RawError:
    if not result.is_error:
        raise ValueError("MCP result is not an error")

    for item in result.content:
        if item.type =="text":
            return RawError(
                message= item.text
            )
    return RawError(
        message= "MCP tool failed without text error content"
    )