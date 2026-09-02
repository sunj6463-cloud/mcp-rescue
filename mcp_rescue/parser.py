from mcp_rescue.models import RawError

def parse_error(error) -> RawError:
    if isinstance(error, str):
        return RawError(
            message=error
        )

    if isinstance(error, dict):

        if "status" in error and "message" in error:
            message = f"{error['status']} {error['message']}"
            return RawError(
                message=message
            )
        elif "message" in error:
            return RawError(
                message=error["message"]
            )
    return RawError(
        message=str(error)
    )    
    