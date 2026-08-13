#!/usr/bin/env python3
"""Bootstrap the sample app: sync deps and create/update .env.

Usage:
    uv run setup.py
    uv run setup.py <LD_SDK_KEY> <CONFIG_KEY>
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_EXAMPLE = ROOT / ".env.example"
ENV_FILE = ROOT / ".env"


def upsert_env(content: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}=.*$", re.MULTILINE)
    line = f"{key}={value}"
    if pattern.search(content):
        return pattern.sub(line, content, count=1)
    return content.rstrip("\n") + f"\n{line}\n"


def ensure_env(sdk_key: str | None, config_key: str | None) -> None:
    if not ENV_FILE.exists():
        if not ENV_EXAMPLE.exists():
            raise FileNotFoundError(f"Missing {ENV_EXAMPLE}")
        shutil.copy(ENV_EXAMPLE, ENV_FILE)
        print(f"Created {ENV_FILE} from .env.example")
    else:
        print(f"Using existing {ENV_FILE}")

    if not sdk_key and not config_key:
        print("Fill in CONFIG_KEY, LD_SDK_KEY, and your provider API keys.")
        return

    content = ENV_FILE.read_text(encoding="utf-8")
    if sdk_key:
        content = upsert_env(content, "LD_SDK_KEY", sdk_key)
        print("Set LD_SDK_KEY in .env")
    if config_key:
        content = upsert_env(content, "CONFIG_KEY", config_key)
        print("Set CONFIG_KEY in .env")
    ENV_FILE.write_text(content, encoding="utf-8")


def main() -> int:
    sdk_key = sys.argv[1].strip() if len(sys.argv) > 1 else None
    config_key = sys.argv[2].strip() if len(sys.argv) > 2 else None

    if len(sys.argv) == 2:
        print(
            "Usage: uv run setup.py [<LD_SDK_KEY> <CONFIG_KEY>]",
            file=sys.stderr,
        )
        print("Provide both keys, or neither.", file=sys.stderr)
        return 1

    print("Syncing dependencies with uv...")
    result = subprocess.run(["uv", "sync"], cwd=ROOT)
    if result.returncode != 0:
        print("uv sync failed.", file=sys.stderr)
        return result.returncode

    try:
        ensure_env(sdk_key or None, config_key or None)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    print("\nSetup complete. Run:")
    print('  uv run main.py "Your question here"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
