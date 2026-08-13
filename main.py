"""
Thin sample entrypoint for the LaunchDarkly Python AI SDK.

Usage:
    uv run main.py "What is feature flagging?"
"""

from __future__ import annotations

import asyncio
import os
import sys
from secrets import token_hex

from dotenv import load_dotenv

load_dotenv()

from launchdarkly_ai_python import (  # noqa: E402
    config,
    global_registry,
    init_client,
    shutdown,
)


def _new_context() -> dict[str, str]:
    return {"kind": "user", "key": token_hex(8)}


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        print(
            f"Missing {name}. Set it in .env (created by `uv run setup.py`).",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return value


async def main() -> None:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print('Usage: uv run main.py "Your question here"', file=sys.stderr)
        raise SystemExit(1)

    question = sys.argv[1].strip()
    config_key = _require_env("CONFIG_KEY")
    _require_env("LD_SDK_KEY")

    # Side-effect: register all provider handlers + tools
    import register  # noqa: F401, E402

    await init_client()

    result = await config(
        key=config_key,
        registry=global_registry,
    ).invoke(question, _new_context())

    print(result.response)
    await shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        sys.stdout.flush()
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
