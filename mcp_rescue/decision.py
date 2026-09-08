from mcp_rescue.models import (
    ErrorCategory,
    RecoveryAction,
    NormalizedError,
    RecoveryDecision,
    ToolInfo
)
def is_safe_to_retry(tool: ToolInfo | None) -> bool:
    if tool is None:
        return False
    elif tool.destructive:
        return False
    elif tool.read_only:
        return True
    elif tool.idempotent:
        return True
    else:
        return False

def decide(error:NormalizedError ,tool: ToolInfo) ->RecoveryDecision:
    if error.category == ErrorCategory.RATE_LIMIT:
        return RecoveryDecision(
            action=RecoveryAction.BACKOFF,
            retryable=True,
            reason="rate limit exceeded, retry after waiting",
        )
    elif error.category == ErrorCategory.AUTHENTICATION:
        return RecoveryDecision(
            action=RecoveryAction.REAUTHENTICATE,
            retryable=False,
            reason="authentication failed, refresh credentials",

        )
    elif error.category == ErrorCategory.PERMISSION:
        return RecoveryDecision(
            action=RecoveryAction.STOP,
            retryable=False,
            reason="permission denied, user authorization required",
        )
    elif error.category == ErrorCategory.NOT_FOUND:
        return RecoveryDecision(
            action=RecoveryAction.STOP,
            retryable=False, 
            reason="resource not found",          
        )
    elif error.category == ErrorCategory.INVALID_ARGUMENT:
        return RecoveryDecision(
            action=RecoveryAction.REPAIR_ARGUMENTS,
            retryable=False,
            reason="invalid input arguments need correction",                       
        )
    elif error.category == ErrorCategory.TRANSIENT_NETWORK:

        if is_safe_to_retry(tool):
            return RecoveryDecision(
                action=RecoveryAction.RETRY,
                retryable=True,
                reason="network error and tool operation is safe to retry",
            )

        else:
            return RecoveryDecision(
                action=RecoveryAction.ASK_USER,
                retryable=False,
                reason="network error but tool is unsafe to retry",
            )

    elif error.category == ErrorCategory.UPSTREAM_UNAVAILABLE:
        return RecoveryDecision(
        action=RecoveryAction.BACKOFF,
        retryable=True,
        reason="upstream service unavailable, retry with backoff",            
        )
    elif error.category == ErrorCategory.BUSINESS_RULE:
        return RecoveryDecision(
        action=RecoveryAction.ASK_USER,
        retryable=False,
        reason="business rule violation requires user decision",

        )
    else:
        return RecoveryDecision(
        action=RecoveryAction.STOP,
        retryable=False,
        reason="unknown error type, unsafe to recover automatically",
        )