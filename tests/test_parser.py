from mcp_rescue.models import RawError
from mcp_rescue.parser import parse_error

def test_parse_string_error():
    error = "429 Too Many Requests"
    result = parse_error(error)
    assert result.message == "429 Too Many Requests"

def test_parse_dict_error():
    error = {
    "code": 401,
    "message": "Unauthorized"
}
    result = parse_error(error)
    assert result.message == "Unauthorized"

def test_parse_exception_error():
    error = TimeoutError("connection timeout")
    result = parse_error(error)
    assert result.message == "connection timeout"


