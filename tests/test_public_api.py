from types import SimpleNamespace

from mcp_rescue.api import rescue_mcp_result
from mcp_rescue.models import (
    ErrorCategory,
    RecoveryAction,
    ToolInfo,
)


def test_rescue_mcp_result():
    result = SimpleNamespace(
        is_error=True,
        content=[
            SimpleNamespace(
                type="text",
                text="connection timeout",
            )
        ],
    )

    tool = ToolInfo(
        name="get_weather",
        read_only=True,
        idempotent=True,
        destructive=False,
    )

    rescued = rescue_mcp_result(
        result,
        tool,
    )

    assert rescued.category == ErrorCategory.TRANSIENT_NETWORK
    assert rescued.action == RecoveryAction.RETRY
    assert rescued.retryable is True