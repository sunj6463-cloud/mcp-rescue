from mcp_rescue.models import ErrorCategory, NormalizedError


def normalize_error(message: str) -> NormalizedError:
    text = message.lower()
    if "429" in text or "rate limit" in text:
        return NormalizedError(
            category=ErrorCategory.RATE_LIMIT,
  
            
            message = message,
            confidence = 1

        )
    elif "401" in text or "unauthorized" in text:
        return NormalizedError(
            category=ErrorCategory.AUTHENTICATION,

            
            message = message,
            confidence = 1.0
        )
    elif "403" in text or "forbidden" in text or "permission denied" in text:
        return NormalizedError(
            category=ErrorCategory.PERMISSION,

           
            message = message,
            confidence = 1.0
        )
    elif "404" in text or "not found" in text:
        return NormalizedError(
            category=ErrorCategory.NOT_FOUND,

            message = message,
            confidence = 1.0
        )
    elif "invalid argument" in text or "bad request" in text:
        return NormalizedError(
            category=ErrorCategory.INVALID_ARGUMENT,

     
            message = message,
            confidence = 1.0
        )

    elif "transient network" in text or "network error" in text or "connection reset" in text or "connection refused" in text or "timed out" in text or "timeout" in text or "DNS failure" in text or "temporary failure" in text:
        return NormalizedError(
            category=ErrorCategory.TRANSIENT_NETWORK,

       
            message = message,
            confidence = 1.0
        )
    elif "upstream unavailable" in text or "service unavailable" in text or "503" in text or "502" in text:  
        return NormalizedError(
            category=ErrorCategory.UPSTREAM_UNAVAILABLE,

            message = message,
            confidence = 1.0
        )

    elif "booking date must be in the future" in text :
        return NormalizedError(
            category=ErrorCategory.BUSINESS_RULE,

            message = message,
            confidence= 1.0)

    else:       
        return NormalizedError(
            category=ErrorCategory.UNKNOWN,

            message = message,
            confidence = 0
        )