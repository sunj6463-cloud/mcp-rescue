from mcp_rescue.models import ErrorCategory, RecoveryAction, RescueError,RawError
from mcp_rescue.normalizer import normalize_error
from mcp_rescue.decision import decide
from mcp_rescue.parser import parse_error

def rescue_error(error,tool) -> RescueError:
    raw = parse_error(error)


    normalized = normalize_error(raw.message)
    decision = decide(normalized,tool)
    
    return RescueError(

    category = normalized.category,

    message= normalized.message,
    confidence= normalized.confidence,
    action = decision.action,
    retryable=  decision.retryable        
    )    

