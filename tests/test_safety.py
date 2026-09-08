from mcp_rescue.models import ToolInfo ,NormalizedError,ErrorCategory,RecoveryAction
from mcp_rescue.decision import decide
def test_tool_info():
    tool = ToolInfo(
        name="send_email",
        read_only=False,
        idempotent=False,
        destructive=True,
    )

    assert tool.destructive is True


def test_tool_get_weather():
    tool = ToolInfo(
    name="get_weather",
    read_only=True,
    idempotent=True,
    destructive=False,
) 
    error = NormalizedError(
    category=ErrorCategory.TRANSIENT_NETWORK,
    message="timeout",
    confidence=1.0,
)   
    result = decide(error, tool)
    assert result.action == RecoveryAction.RETRY
    assert result.retryable is True

    tool = ToolInfo(
    name="send_email",
    read_only=False,
    idempotent=False,
    destructive=False,
)
    result = decide(error, tool)
    assert result.action == RecoveryAction.ASK_USER
    assert result.retryable is False