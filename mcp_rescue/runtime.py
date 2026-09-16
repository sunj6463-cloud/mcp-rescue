from mcp_rescue.models import RecoveryAction, RescueError

def allow_automatic_retry(rescued: RescueError)-> bool:
    if not rescued.retryable:
        return False
    if rescued.action not in {
        RecoveryAction.RETRY,
        RecoveryAction.BACKOFF
    }:
        return False

    return True