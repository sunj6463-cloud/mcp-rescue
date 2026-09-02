from mcp_rescue.models import ErrorCategory, RecoveryAction, RescueError
from mcp_rescue.normalizer import normalize_error
from mcp_rescue.decision import decide
from mcp_rescue.parser import parse_error

def rescue_error(error) -> RescueError:
    raw = parse_error(error)


    normalized = normalize_error(raw.message)
    decision = decide(normalized)
    
    return RescueError(

    category = normalized.category,

    message= normalized.message,
    confidence= normalized.confidence,
    action = decision.action,
    retryable=  decision.retryable        
    )    

print (rescue_error(    {
        "status":429,
        "message":"Too Many Requests"
    }))