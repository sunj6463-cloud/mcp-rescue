from mcp_rescue.models import RescueError, ErrorCategory, RecoveryAction
def test_rescue_error_creation():
    error = RescueError(
        category=ErrorCategory.RATE_LIMIT,
        action=RecoveryAction.BACKOFF,
        retryable=True,
        message="Rate limit exceeded. Please try again later.",
        confidence=0.95
    )
    assert error.category == ErrorCategory.RATE_LIMIT
    assert error.action == RecoveryAction.BACKOFF
    assert error.retryable is True
    assert error.message == "Rate limit exceeded. Please try again later."
    assert error.confidence == 0.95
    