from mcp_rescue.models import (
    ErrorCategory,
    RecoveryAction,
    NormalizedError,
    RecoveryDecision,
)


def decide(error:NormalizedError) ->RecoveryDecision:
    if error.category == ErrorCategory.RATE_LIMIT:
        return RecoveryDecision(
            action=RecoveryAction.BACKOFF,
            retryable=True,
        )
    elif error.category == ErrorCategory.AUTHENTICATION:
        return RecoveryDecision(
            action=RecoveryAction.REAUTHENTICATE,
            retryable=False,

        )
    elif error.category == ErrorCategory.PERMISSION:
        return RecoveryDecision(
            action=RecoveryAction.STOP,
            retryable=False,
        )
    elif error.category == ErrorCategory.NOT_FOUND:
        return RecoveryDecision(
            action=RecoveryAction.STOP,
            retryable=False,           
        )
    elif error.category == ErrorCategory.INVALID_ARGUMENT:
        return RecoveryDecision(
            action=RecoveryAction.REPAIR_ARGUMENTS,
            retryable=False,                       
        )
    elif error.category == ErrorCategory.TRANSIENT_NETWORK:
        return RecoveryDecision(
            action=RecoveryAction.RETRY,
            retryable=True,           
        )

    elif error.category == ErrorCategory.UPSTREAM_UNAVAILABLE:
        return RecoveryDecision(
        action=RecoveryAction.BACKOFF,
        retryable=True,            
        )
    elif error.category == ErrorCategory.BUSINESS_RULE:
        return RecoveryDecision(
        action=RecoveryAction.ASK_USER,
        retryable=False,

        )
    else:
        return RecoveryDecision(
        action=RecoveryAction.STOP,
        retryable=False,

        )