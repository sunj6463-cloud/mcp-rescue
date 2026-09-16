from types import SimpleNamespace

from mcp_rescue.adapters.mcp import parse_mcp_result
from mcp_rescue.classifier import rescue_error
from mcp_rescue.models import (
    ErrorCategory,
    RecoveryAction,
    ToolInfo,
)


def make_mcp_error(message: str):
    return SimpleNamespace(
        is_error=True,
        content=[
            SimpleNamespace(
                type="text",
                text=message,
            )
        ],
    )


def test_rate_limit_pipeline():
    result = make_mcp_error(
        "Error executing tool rate_limited: 429 Too Many Requests"
    )

    raw = parse_mcp_result(result)

    tool = ToolInfo(
        name="rate_limited",
        read_only=True,
        idempotent=True,
        destructive=False,
    )

    rescued = rescue_error(raw, tool)

    assert rescued.category == ErrorCategory.RATE_LIMIT
    assert rescued.action == RecoveryAction.BACKOFF
    assert rescued.retryable is True


def test_business_rule_pipeline():
    result = make_mcp_error(
        "Error executing tool booking: "
        "Booking date must be in the future"
    )

    raw = parse_mcp_result(result)

    tool = ToolInfo(
        name="booking",
        read_only=False,
        idempotent=False,
        destructive=False,
    )

    rescued = rescue_error(raw, tool)

    assert rescued.category == ErrorCategory.BUSINESS_RULE
    assert rescued.action == RecoveryAction.ASK_USER
    assert rescued.retryable is False


def test_timeout_read_only_tool_can_retry():
    result = make_mcp_error(
        "Error executing tool weather_timeout: connection timeout"
    )

    raw = parse_mcp_result(result)

    tool = ToolInfo(
        name="weather_timeout",
        read_only=True,
        idempotent=True,
        destructive=False,
    )

    rescued = rescue_error(raw, tool)

    assert rescued.category == ErrorCategory.TRANSIENT_NETWORK
    assert rescued.action == RecoveryAction.RETRY
    assert rescued.retryable is True


def test_timeout_non_idempotent_tool_cannot_retry():
    result = make_mcp_error(
        "Error executing tool send_email_timeout: connection timeout"
    )

    raw = parse_mcp_result(result)

    tool = ToolInfo(
        name="send_email_timeout",
        read_only=False,
        idempotent=False,
        destructive=False,
    )

    rescued = rescue_error(raw, tool)

    assert rescued.category == ErrorCategory.TRANSIENT_NETWORK
    assert rescued.action == RecoveryAction.ASK_USER
    assert rescued.retryable is False