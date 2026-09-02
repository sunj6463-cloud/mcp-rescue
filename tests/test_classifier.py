from mcp_rescue.classifier import rescue_error
from mcp_rescue.models import ErrorCategory, RecoveryAction, RescueError

# def test_classify_error_rate_limit():
#     result = classify_error("429 Too Many Requests")
#     assert result.category == ErrorCategory.RATE_LIMIT
#     assert result.action == RecoveryAction.BACKOFF
#     assert result.retryable is True
#     assert result.message == "429 Too Many Requests"

# def test_classify_error_unknown():
#     result = classify_error("unknown")
#     assert result.category == ErrorCategory.UNKNOWN
#     assert result.action == RecoveryAction.STOP
#     assert result.retryable is False

# def test_classify_error_authentication():
#     result = classify_error("401 Unauthorized")
#     assert result.category == ErrorCategory.AUTHENTICATION 
#     assert result.action == RecoveryAction.REAUTHENTICATE
#     assert result.retryable is False
#     assert result.message == "401 Unauthorized"

# def test_classify_error_authentication_code():
#     result = classify_error("401")
#     assert result.category == ErrorCategory.AUTHENTICATION 
#     assert result.action == RecoveryAction.REAUTHENTICATE
#     assert result.retryable is False

# def test_classify_error_permission():
#     result = classify_error("403 Forbidden")
#     assert result.category == ErrorCategory.PERMISSION
#     assert result.action == RecoveryAction.STOP
#     assert result.retryable is False
#     assert result.message == "403 Forbidden"

# def test_classify_error_not_found():
#     result = classify_error("404 Not Found")
#     assert result.category == ErrorCategory.NOT_FOUND
#     assert result.action == RecoveryAction.STOP
#     assert result.retryable is False
#     assert result.message == "404 Not Found"

# def test_classify_error_invalid_argument():
#     result = classify_error("Invalid argument provided")
#     assert result.category == ErrorCategory.INVALID_ARGUMENT
#     assert result.action == RecoveryAction.REPAIR_ARGUMENTS
#     assert result.retryable is False
#     assert result.message == "Invalid argument provided"

# def test_classify_error_bad_request():
#     result = classify_error("400 Bad Request")
#     assert result.category == ErrorCategory.INVALID_ARGUMENT
#     assert result.action == RecoveryAction.REPAIR_ARGUMENTS
#     assert result.retryable is False
#     assert result.message == "400 Bad Request"

# def test_classify_error_transient_network():
#     result = classify_error("Transient network error occurred")
#     assert result.category == ErrorCategory.TRANSIENT_NETWORK
#     assert result.action == RecoveryAction.RETRY
#     assert result.retryable is True
#     assert result.message == "Transient network error occurred"


# def test_classify_error_upstream_unavailable():
#     result = classify_error("503 Service Unavailable")
#     assert result.category == ErrorCategory.UPSTREAM_UNAVAILABLE
#     assert result.action == RecoveryAction.BACKOFF
#     assert result.retryable is True
#     assert result.message == "503 Service Unavailable"


# def test_classify_error_upstream_unavailable_code():
#     result = classify_error("502")
#     assert result.category == ErrorCategory.UPSTREAM_UNAVAILABLE
#     assert result.action == RecoveryAction.BACKOFF
#     assert result.retryable is True
#     assert result.message == "502"


# def test_classify_error_upstream_unavailable_service():
#     result = classify_error("Service Unavailable")
#     assert result.category == ErrorCategory.UPSTREAM_UNAVAILABLE
#     assert result.action == RecoveryAction.BACKOFF
#     assert result.retryable is True
#     assert result.message == "Service Unavailable"


# def test_classify_error_upstream_unavailable_business_rule():
#     result = classify_error("Booking date must be in the future")
#     assert result.category == ErrorCategory.BUSINESS_RULE
#     assert result.action == RecoveryAction.ASK_USER
#     assert result.retryable is False
#     assert result.confidence == 1.0
#     assert result.message == "Booking date must be in the future"







def test_rescue_error_rate_limit():
    result = rescue_error("429 Too Many Requests")
    assert result.category == ErrorCategory.RATE_LIMIT
    assert result.action == RecoveryAction.BACKOFF
    assert result.retryable is True
    assert result.message == "429 Too Many Requests"

def test_rescue_error_unknown():
    result = rescue_error("unknown")
    assert result.category == ErrorCategory.UNKNOWN
    assert result.action == RecoveryAction.STOP
    assert result.retryable is False

def test_rescue_error_authentication():
    result = rescue_error("401 Unauthorized")
    assert result.category == ErrorCategory.AUTHENTICATION 
    assert result.action == RecoveryAction.REAUTHENTICATE
    assert result.retryable is False
    assert result.message == "401 Unauthorized"

def test_rescue_error_authentication_code():
    result = rescue_error("401")
    assert result.category == ErrorCategory.AUTHENTICATION 
    assert result.action == RecoveryAction.REAUTHENTICATE
    assert result.retryable is False

def test_rescue_error_permission():
    result = rescue_error("403 Forbidden")
    assert result.category == ErrorCategory.PERMISSION
    assert result.action == RecoveryAction.STOP
    assert result.retryable is False
    assert result.message == "403 Forbidden"

def test_rescue_error_not_found():
    result = rescue_error("404 Not Found")
    assert result.category == ErrorCategory.NOT_FOUND
    assert result.action == RecoveryAction.STOP
    assert result.retryable is False
    assert result.message == "404 Not Found"

def test_rescue_error_invalid_argument():
    result = rescue_error("Invalid argument provided")
    assert result.category == ErrorCategory.INVALID_ARGUMENT
    assert result.action == RecoveryAction.REPAIR_ARGUMENTS
    assert result.retryable is False
    assert result.message == "Invalid argument provided"

def test_rescue_error_bad_request():
    result = rescue_error("400 Bad Request")
    assert result.category == ErrorCategory.INVALID_ARGUMENT
    assert result.action == RecoveryAction.REPAIR_ARGUMENTS
    assert result.retryable is False
    assert result.message == "400 Bad Request"

def test_rescue_error_transient_network():
    result = rescue_error("Transient network error occurred")
    assert result.category == ErrorCategory.TRANSIENT_NETWORK
    assert result.action == RecoveryAction.RETRY
    assert result.retryable is True
    assert result.message == "Transient network error occurred"


def test_rescue_error_upstream_unavailable():
    result = rescue_error("503 Service Unavailable")
    assert result.category == ErrorCategory.UPSTREAM_UNAVAILABLE
    assert result.action == RecoveryAction.BACKOFF
    assert result.retryable is True
    assert result.message == "503 Service Unavailable"


def test_rescue_error_upstream_unavailable_code():
    result = rescue_error("502")
    assert result.category == ErrorCategory.UPSTREAM_UNAVAILABLE
    assert result.action == RecoveryAction.BACKOFF
    assert result.retryable is True
    assert result.message == "502"


def test_rescue_error_upstream_unavailable_service():
    result = rescue_error("Service Unavailable")
    assert result.category == ErrorCategory.UPSTREAM_UNAVAILABLE
    assert result.action == RecoveryAction.BACKOFF
    assert result.retryable is True
    assert result.message == "Service Unavailable"


def test_rescue_error_upstream_unavailable_business_rule():
    result = rescue_error("Booking date must be in the future")
    assert result.category == ErrorCategory.BUSINESS_RULE
    assert result.action == RecoveryAction.ASK_USER
    assert result.retryable is False
    assert result.confidence == 1.0
    assert result.message == "Booking date must be in the future"

def test_rescue_error_from_http_dict():
    result = rescue_error(
        {
            "status":429,
            "message":"Too Many Requests"
        }
    )

    assert result.category == ErrorCategory.RATE_LIMIT
    assert result.action == RecoveryAction.BACKOFF