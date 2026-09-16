from types import SimpleNamespace
import pytest
from mcp_rescue.adapters.mcp import parse_mcp_result
from mcp_rescue.models import RawError
def test_parse_mcp_error_text():
    result = SimpleNamespace(
        is_error=True,
        content=[
            SimpleNamespace(
                type="text",
                text="429 Too Many Requests",
            )
        ],
    )

    raw = parse_mcp_result(result)

    assert isinstance(raw, RawError)
    assert raw.message == "429 Too Many Requests"


def test_parse_success_result_should_fail():
    result = SimpleNamespace(
        is_error=False,
        content=[
            SimpleNamespace(
                type="text",
                text="success",
            )
        ],
    )

    with pytest.raises(ValueError):
        parse_mcp_result(result)


def test_parse_mcp_error_without_text():
    result = SimpleNamespace(
        is_error=True,
        content=[],
    )

    raw = parse_mcp_result(result)

    assert isinstance(raw, RawError)
    assert raw.message == "MCP tool failed without text error content"