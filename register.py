"""Populate the global registry with all provider handlers and an example tool."""

from __future__ import annotations

import os

# Handler factories construct provider clients at register time.
# Placeholders let unused providers load; the selected provider still needs a real key.
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "unset"
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = "unset"

from launchdarkly_ai_claude_agents import create_claude_agents_handler
from launchdarkly_ai_claude_messages import create_claude_messages_handler
from launchdarkly_ai_langchain_agents import create_langchain_agents_handler
from launchdarkly_ai_langchain_messages import create_langchain_messages_handler
from launchdarkly_ai_openai_agents import create_openai_agent_handler
from launchdarkly_ai_openai_messages import create_openai_messages_handler
from launchdarkly_ai_python import global_registry


async def example_tool(_args: dict) -> str:
    """Minimal example tool for configs that reference tools."""
    return "tool called"


global_registry.register(
    handlers=[
        create_openai_messages_handler(),
        create_openai_agent_handler(),
        create_claude_agents_handler(),
        create_claude_messages_handler(),
        create_langchain_messages_handler(),
        create_langchain_agents_handler(),
    ],
    tools={
        "example-tool": example_tool,
    },
)
