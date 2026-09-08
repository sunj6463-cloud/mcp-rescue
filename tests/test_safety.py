from mcp_rescue.models import (
    ToolInfo,
    NormalizedError,
    ErrorCategory,
    RecoveryAction,
)
from mcp_rescue.decision import decide
from mcp_rescue.classifier import rescue_error
def  test_create_tool_info():
    tool = ToolInfo(
        name="send_email",
        read_only=False,
        idempotent=False,
        destructive=True,
    )

    assert tool.destructive is True



def test_destructive_tool_should_not_retry():

    tool = ToolInfo(
    name= "delete_file",
    idempotent=True,
    destructive=True,
    read_only= False

    )
    error = NormalizedError(
    category=ErrorCategory.TRANSIENT_NETWORK,
    message="timeout",
    confidence=1.0,
    )   
    result = decide(error, tool)
    assert result.action == RecoveryAction.ASK_USER
    assert result.retryable is False


def test_safe_retry_readonly():
    
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

def test_non_idempotent_tool_should_not_retry():
    tool = ToolInfo(
    name="send_email",
    read_only=False,
    idempotent=False,
    destructive=False,
)
    error = NormalizedError(
        category=ErrorCategory.TRANSIENT_NETWORK,
        message="timeout",
        confidence=1.0,
    )   
    result = decide(error, tool)
    assert result.action == RecoveryAction.ASK_USER
    assert result.retryable is False


def test_rescue_error_with_tool_context():
    tool = ToolInfo(
    name="get_weather",
    read_only=True,
    idempotent=True,
    destructive=False,
)

    result = rescue_error(
        "connection timeout",
        tool
    )

    assert result.action == RecoveryAction.RETRY
    assert result.retryable is True