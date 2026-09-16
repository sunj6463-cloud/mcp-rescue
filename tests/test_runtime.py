from mcp_rescue.models import (
    ErrorCategory,
    RecoveryAction,
    RescueError,
)
from mcp_rescue.runtime import allow_automatic_retry


def test_retry_action_can_retry():
    rescued = RescueError(
        category=ErrorCategory.TRANSIENT_NETWORK,
        action=RecoveryAction.RETRY,
        retryable=True,
        message="connection timeout",
        confidence=1.0,
    )

    assert allow_automatic_retry(rescued) is True


def test_backoff_action_can_retry():
    rescued = RescueError(
        category=ErrorCategory.RATE_LIMIT,
        action=RecoveryAction.BACKOFF,
        retryable=True,
        message="429 Too Many Requests",
        confidence=1.0,
    )

    assert allow_automatic_retry(rescued) is True


def test_ask_user_cannot_retry():
    rescued = RescueError(
        category=ErrorCategory.BUSINESS_RULE,
        action=RecoveryAction.ASK_USER,
        retryable=False,
        message="Booking date must be in the future",
        confidence=1.0,
    )

    assert allow_automatic_retry(rescued) is False


def test_retryable_true_but_wrong_action_cannot_retry():
    rescued = RescueError(
        category=ErrorCategory.BUSINESS_RULE,
        action=RecoveryAction.ASK_USER,
        retryable=True,
        message="conflicting recovery decision",
        confidence=1.0,
    )

    assert allow_automatic_retry(rescued) is False