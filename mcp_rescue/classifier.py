from mcp_rescue.models import ErrorCategory, RecoveryAction, RescueError
from mcp_rescue.normalizer import normalize_error
from mcp_rescue.decision import decide
# def classify_error(message:str) -> RescueError:
#     text = message.lower()
#     if "429" in text or "rate limit" in text:
#         return RescueError(
#             category=ErrorCategory.RATE_LIMIT,
#             action=RecoveryAction.BACKOFF,
#             retryable=True,
#             message = message,
#             confidence = 1

#         )
#     elif "401" in text or "unauthorized" in text:
#         return RescueError(
#             category=ErrorCategory.AUTHENTICATION,
#             action=RecoveryAction.REAUTHENTICATE,
#             retryable=False,
#             message = message,
#             confidence = 1.0
#         )
#     elif "403" in text or "forbidden" in text or "permission denied" in text:
#         return RescueError(
#             category=ErrorCategory.PERMISSION,
#             action=RecoveryAction.STOP,
#             retryable=False,
#             message = message,
#             confidence = 1.0
#         )
#     elif "404" in text or "not found" in text:
#         return RescueError(
#             category=ErrorCategory.NOT_FOUND,
#             action=RecoveryAction.STOP,
#             retryable=False,
#             message = message,
#             confidence = 1.0
#         )
#     elif "invalid argument" in text or "bad request" in text:
#         return RescueError(
#             category=ErrorCategory.INVALID_ARGUMENT,
#             action=RecoveryAction.REPAIR_ARGUMENTS,
#             retryable=False,
#             message = message,
#             confidence = 1.0
#         )

#     elif "transient network" in text or "network error" in text or "connection reset" in text or "connection refused" in text or "timed out" in text or "timeout" in text or "DNS failure" in text or "temporary failure" in text:
#         return RescueError(
#             category=ErrorCategory.TRANSIENT_NETWORK,
#             action=RecoveryAction.RETRY,
#             retryable=True,
#             message = message,
#             confidence = 1.0
#         )
#     elif "upstream unavailable" in text or "service unavailable" in text or "503" in text or "502" in text:  
#         return RescueError(
#             category=ErrorCategory.UPSTREAM_UNAVAILABLE,
#             action=RecoveryAction.BACKOFF,
#             retryable=True,
#             message = message,
#             confidence = 1.0
#         )

#     elif "booking date must be in the future" in text :
#         return RescueError(
#             category=ErrorCategory.BUSINESS_RULE,
#             action=RecoveryAction.ASK_USER,
#             retryable=False,
#             message = message,
#             confidence= 1.0)

#     else:       
#         return RescueError(
#             category=ErrorCategory.UNKNOWN,
#             action=RecoveryAction.STOP,
#             retryable=False,
#             message = message,
#             confidence = 0
#         )

def rescue_error(message:str) -> RescueError:
    text = message.lower()

    normalized = normalize_error(message)
    decision = decide(normalized)
    
    return RescueError(

    category = normalized.category,

    message= normalized.message,
    confidence= normalized.confidence,
    action = decision.action,
    retryable=  decision.retryable        
    )
