# hello-agentcontrol-python

Hello LaunchDarkly for the [Python Agent Control SDK](https://github.com/launchdarkly/python-ai-sdk).

Thin sample that wires every provider handler and asks LaunchDarkly which one to use at runtime. Observability (OpenTelemetry) is installed and auto-configured via `init_client()`.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Clone

```bash
git clone https://github.com/launchdarkly/hello-agentcontrol-python.git
cd hello-agentcontrol-python
```

## Setup

```bash
# Install deps and create a blank .env
uv run setup.py

# Or pass your LaunchDarkly keys and have setup write them into .env:
uv run setup.py <LD_SDK_KEY> <CONFIG_KEY>
```

Example:

```bash
uv run setup.py sdk-xxxxxxxxxxxxxxxxxxxxxxxx my-ai-config
```

This syncs dependencies and creates `.env` from `.env.example` if missing. When both arguments are provided, `LD_SDK_KEY` and `CONFIG_KEY` are inserted (or updated) in `.env`. Provide both keys, or neither.

Still fill in provider keys as needed:

- `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY` — whichever providers your config may select

## Run

```bash
uv run main.py "What is feature flagging?"
```

LaunchDarkly chooses the provider and model from your AI config. Traces export to LaunchDarkly Observability automatically (no extra app code).
