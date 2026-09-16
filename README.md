# MCP-Rescue

A lightweight semantic recovery layer for MCP tool failures.

MCP-Rescue turns MCP tool errors into structured recovery decisions. It combines error classification with tool metadata so an agent or runtime can decide whether to retry, repair arguments, ask the user, or stop.

## Why MCP-Rescue?

**Same error, different tool semantics, different recovery decisions.**

Both of these tools can fail with `connection timeout`, but retrying them has different consequences:

| Tool | Read-only | Idempotent | Destructive | Recovery decision |
| --- | --- | --- | --- | --- |
| `get_weather` | `True` | `True` | `False` | `RETRY` |
| `send_email` | `False` | `False` | `False` | `ASK_USER` |

Retrying a weather query is usually safe. Retrying an email operation after a timeout may send the same email twice: the original request might have succeeded before the connection failed.

MCP-Rescue makes that distinction explicit and returns a decision your runtime can enforce.

## Local setup

Use Python 3.10 or later. The current development environment uses Python 3.14.3 and `mcp==2.2.0`.

From the repository root, create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```


## Installation

Install MCP-Rescue from PyPI:

```bash
python -m pip install mcp-rescue

For development:

python -m pip install "mcp-rescue[dev]"

For the Qwen demo:

python -m pip install "mcp-rescue[qwen]"

After installation, you can use MCP-Rescue in your Python project.


## Quick start

This example uses a sample failed MCP result and runs without an MCP server or an API key:

```python
from mcp.types import CallToolResult, TextContent

from mcp_rescue.api import rescue_mcp_result
from mcp_rescue.models import ToolInfo
from mcp_rescue.runtime import allow_automatic_retry


tool = ToolInfo(
    name="get_weather",
    read_only=True,
    idempotent=True,
    destructive=False,
)

result = CallToolResult(
    is_error=True,
    content=[TextContent(type="text", text="connection timeout")],
)

if result.is_error:
    rescued = rescue_mcp_result(result, tool)

    print(rescued.category)
    print(rescued.action)
    print(rescued.retryable)

    if allow_automatic_retry(rescued):
        print("Automatic retry is allowed.")
```

Output:

```text
ErrorCategory.TRANSIENT_NETWORK
RecoveryAction.RETRY
True
Automatic retry is allowed.
```

For an actual tool call, use the same error check inside your async code with an initialized MCP client:

```python
result = await mcp_client.call_tool("get_weather", {})

if result.is_error:
    rescued = rescue_mcp_result(result, tool)
    automatic_retry_allowed = allow_automatic_retry(rescued)
    # Let your runtime handle the decision and enforce retry limits.
```

`rescue_mcp_result()` handles failed results only. Passing a successful result raises `ValueError`. The current adapter expects the `is_error` attribute used by the MCP dependency above and reads the first text content block.

For error strings, exceptions, or dictionaries, use the lower-level API:

```python
from mcp_rescue.classifier import rescue_error

rescued = rescue_error("connection timeout", tool)
```

## How it works

```text
Agent / LLM
    |
    v
MCP client -> MCP tool -> Failed result
                              |
                              v
                         MCP-Rescue
                         1. Parse the error
                         2. Normalize and classify
                         3. Decide recovery using the error and tool metadata
                              |
                              v
                         RescueError
                              |
                              v
                         Agent / Runtime
```

Each `RescueError` contains:

| Field | Meaning |
| --- | --- |
| `category` | What kind of failure occurred. |
| `action` | What the caller should do next. |
| `retryable` | Whether the current policy permits a retry. |
| `message` | The error text used for classification. |
| `confidence` | A rule-match score: currently `1.0` for a match and `0.0` for an unknown error. |

Classification currently uses deterministic message-matching rules and requires no LLM call. The runtime remains responsible for executing recovery actions, enforcing retry limits, and choosing backoff delays.

## Recovery decisions

The current policy maps recognized errors as follows:

| Error category | Example message | Recovery action | Retryable |
| --- | --- | --- | --- |
| `RATE_LIMIT` | `429 Too Many Requests` | `BACKOFF` | `True` |
| `INVALID_ARGUMENT` | `Invalid argument` | `REPAIR_ARGUMENTS` | `False` |
| `AUTHENTICATION` | `401 Unauthorized` | `REAUTHENTICATE` | `False` |
| `PERMISSION` | `403 Forbidden` | `STOP` | `False` |
| `NOT_FOUND` | `404 Not Found` | `STOP` | `False` |
| `TRANSIENT_NETWORK` | `connection timeout` | `RETRY` or `ASK_USER` | Depends on tool metadata |
| `UPSTREAM_UNAVAILABLE` | `503 Service Unavailable` | `BACKOFF` | `True` |
| `BUSINESS_RULE` | `Booking date must be in the future` | `ASK_USER` | `False` |
| `UNKNOWN` | An unrecognized error message | `STOP` | `False` |

`REPLAN` is also defined in `RecoveryAction`, but the current policy does not emit it. Business-rule detection currently recognizes the booking message shown above; additional domain rules require extending the normalizer.

## Tool-aware retry safety

For `TRANSIENT_NETWORK` errors, MCP-Rescue checks the caller-supplied `ToolInfo`:

- Missing metadata or a destructive tool produces `ASK_USER` with `retryable=False`.
- A non-destructive tool that is read-only or idempotent produces `RETRY` with `retryable=True`.
- Other tools produce `ASK_USER` with `retryable=False`.

For example, the same timeout with this metadata requires user input:

```python
email_tool = ToolInfo(
    name="send_email",
    read_only=False,
    idempotent=False,
    destructive=False,
)

rescued = rescue_error("connection timeout", email_tool)
print(rescued.action)     # RecoveryAction.ASK_USER
print(rescued.retryable)  # False
```

`allow_automatic_retry(rescued)` returns `True` only when `retryable=True` and the action is `RETRY` or `BACKOFF`. It checks the decision; it does not execute a retry or independently inspect the tool.

**Current policy limit:** tool metadata affects transient network errors only. `RATE_LIMIT` and `UPSTREAM_UNAVAILABLE` currently produce retryable `BACKOFF` decisions regardless of tool metadata. Runtimes handling side effects should apply their own safety checks to those decisions.

## Agent integration

The [Qwen demo](examples/qwen_mcp_demo.py) connects Qwen to the [local MCP demo server](examples/failing_server.py), classifies a failed booking call, and returns a recovery report to the model:

```text
User requests booking(date="2026-01-01")
    -> Qwen requests the booking tool
    -> MCP demo server raises "Booking date must be in the future"
    -> MCP-Rescue returns BUSINESS_RULE / ASK_USER / retryable=False
    -> Qwen receives the recovery report and can ask for a future date
```

The server deliberately rejects that fixed date to demonstrate a business-rule failure.

To run the demo, install the additional dependency:

```bash
python -m pip install "mcp-rescue[qwen]"
```

Set `DASHSCOPE_API_KEY` in your environment, then run from the repository root:

```bash
python -m examples.qwen_mcp_demo
```

This demo makes live Qwen API calls. It shows the first tool call, the recovery report, and the model's follow-up response; it does not implement a full recovery loop.

## Project structure

```text
mcp_rescue/
|-- api.py           # Public MCP result entry point
|-- models.py        # Error categories, actions, and tool metadata
|-- parser.py        # Convert error inputs into RawError
|-- normalizer.py    # Classify error messages
|-- decision.py      # Choose recovery actions
|-- classifier.py    # Compose parsing, normalization, and decisions
|-- runtime.py       # Check whether a decision allows automatic retry
+-- adapters/
    +-- mcp.py       # Extract error text from failed MCP results
examples/           # MCP server, clients, and agent demos
tests/              # Unit and pipeline tests
```

## Development

Run the test suite without external API credentials:

```bash
python -m pytest tests/ -q
```

The suite covers parsing, normalization, recovery decisions, tool-aware retry safety, runtime gating, MCP result adaptation, and the public API. Specifying `tests/` excludes live API example scripts from test discovery.

## Project status

MCP-Rescue is an early-stage project focused on error normalization, structured recovery decisions, and agent integration. MCP-Rescue is currently released as v0.1.0.
Future work includes broader recovery policies, runtime integrations, and more agent framework examples.