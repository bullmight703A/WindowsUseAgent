"""WindowsUseAgent - A Windows Desktop Agent with Modular LLM Providers."""

__version__ = "0.1.0"
__author__ = "WindowsUseAgent Team"
__license__ = "MIT"

from windowsuseagent.agent import WindowsUseAgent
from windowsuseagent.providers.base import BaseLLMProvider
from windowsuseagent.providers.openai_provider import OpenAIProvider
from windowsuseagent.providers.routellm_provider import RouteLLMProvider
from windowsuseagent.providers.anthropic_provider import AnthropicProvider

__all__ = [
    "WindowsUseAgent",
    "BaseLLMProvider",
    "OpenAIProvider",
    "RouteLLMProvider",
    "AnthropicProvider",
]
