from dataclasses import dataclass
from enum import Enum

class ErrorCategory(Enum):
    """Error categories for the MCP Rescue system."""
    RATE_LIMIT = "rate_limit"
    INVALID_ARGUMENT = "invalid_argument"
    AUTHENTICATION = "authentication"
    PERMISSION = "permission"
    NOT_FOUND = "not_found"
    TRANSIENT_NETWORK = "transient_network"
    UPSTREAM_UNAVAILABLE = "upstream_unavailable"
    BUSINESS_RULE = "business_rule"
    UNKNOWN = "unknown"

class RecoveryAction(Enum):
    """Recovery actions for the MCP Rescue system."""
    RETRY = "retry"
    BACKOFF = "backoff"
    REPAIR_ARGUMENTS = "repair_arguments"
    REAUTHENTICATE = "reauthenticate"
    REPLAN = "replan"
    ASK_USER = "ask_user"
    STOP = "stop"

@dataclass
class RescueError:
    category: ErrorCategory
    action: RecoveryAction
    retryable: bool
    message: str
    confidence: float

