"""Core WindowsUseAgent implementation."""

import logging
from typing import Dict, Any, Optional, Type
from windowsuseagent.providers.base import BaseLLMProvider
from windowsuseagent.providers.openai_provider import OpenAIProvider
from windowsuseagent.providers.anthropic_provider import AnthropicProvider
from windowsuseagent.providers.routellm_provider import RouteLLMProvider

logger = logging.getLogger(__name__)


class WindowsUseAgent:
    """Main Windows Use Agent with modular LLM provider support.
    
    This agent provides a flexible interface for interacting with different
    LLM providers, making it easy to switch between OpenAI, Anthropic, RouteLLM,
    and other providers.
    """

    AVAILABLE_PROVIDERS = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "routellm": RouteLLMProvider,
    }

    def __init__(
        self,
        provider_name: str,
        provider_config: Dict[str, Any],
        agent_config: Optional[Dict[str, Any]] = None
    ):
        """Initialize the WindowsUseAgent.
        
        Args:
            provider_name: Name of the LLM provider (openai, anthropic, routellm)
            provider_config: Configuration for the LLM provider
            agent_config: Additional agent configuration (optional)
            
        Raises:
            ValueError: If provider_name is not recognized
        """
        self.provider_name = provider_name.lower()
        self.provider_config = provider_config
        self.agent_config = agent_config or {}
        
        # Initialize the LLM provider
        self.provider = self._initialize_provider()
        
        # Agent state
        self.conversation_history = []
        self.system_prompt = self.agent_config.get(
            "system_prompt",
            "You are a helpful Windows desktop assistant."
        )
        
        logger.info(
            f"WindowsUseAgent initialized with {self.provider.get_provider_name()} "
            f"provider using {self.provider.get_model_name()} model"
        )

    def _initialize_provider(self) -> BaseLLMProvider:
        """Initialize the LLM provider.
        
        Returns:
            Initialized provider instance
            
        Raises:
            ValueError: If provider is not recognized
        """
        if self.provider_name not in self.AVAILABLE_PROVIDERS:
            available = ", ".join(self.AVAILABLE_PROVIDERS.keys())
            raise ValueError(
                f"Unknown provider '{self.provider_name}'. "
                f"Available providers: {available}"
            )
        
        provider_class = self.AVAILABLE_PROVIDERS[self.provider_name]
        return provider_class(self.provider_config)

    def chat(
        self,
        message: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ):
        """Send a message to the agent and get a response.
        
        Args:
            message: User's message
            temperature: Sampling temperature (overrides config)
            max_tokens: Maximum tokens to generate (overrides config)
            stream: Whether to stream the response
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Response string if stream=False, generator if stream=True
        """
        # Use config defaults if not specified
        temperature = temperature or self.agent_config.get("temperature", 0.7)
        max_tokens = max_tokens or self.agent_config.get("max_tokens", 1000)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            if stream:
                return self._stream_response(
                    message, temperature, max_tokens, **kwargs
                )
            else:
                response = self.provider.generate_response(
                    prompt=message,
                    system_prompt=self.system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                
                # Add response to history
                self.conversation_history.append(
                    {"role": "assistant", "content": response}
                )
                
                return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    def _stream_response(self, message: str, temperature: float, max_tokens: int, **kwargs):
        """Stream response from the provider.
        
        Args:
            message: User's message
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Yields:
            Response chunks
        """
        full_response = ""
        
        for chunk in self.provider.generate_streaming_response(
            prompt=message,
            system_prompt=self.system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        ):
            full_response += chunk
            yield chunk
        
        # Add complete response to history
        self.conversation_history.append(
            {"role": "assistant", "content": full_response}
        )

    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.conversation_history = []
        logger.info("Conversation history reset")

    def get_conversation_history(self) -> list:
        """Get the conversation history.
        
        Returns:
            List of conversation messages
        """
        return self.conversation_history.copy()

    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt.
        
        Args:
            prompt: New system prompt
        """
        self.system_prompt = prompt
        logger.info("System prompt updated")

    def get_provider_info(self) -> Dict[str, str]:
        """Get information about the current provider.
        
        Returns:
            Dictionary with provider information
        """
        return {
            "provider": self.provider.get_provider_name(),
            "model": self.provider.get_model_name(),
        }

    @classmethod
    def register_provider(
        cls,
        name: str,
        provider_class: Type[BaseLLMProvider]
    ) -> None:
        """Register a custom LLM provider.
        
        Args:
            name: Provider name
            provider_class: Provider class (must inherit from BaseLLMProvider)
            
        Raises:
            TypeError: If provider_class doesn't inherit from BaseLLMProvider
        """
        if not issubclass(provider_class, BaseLLMProvider):
            raise TypeError(
                f"Provider class must inherit from BaseLLMProvider, "
                f"got {provider_class}"
            )
        
        cls.AVAILABLE_PROVIDERS[name.lower()] = provider_class
        logger.info(f"Registered custom provider: {name}")

    @classmethod
    def list_providers(cls) -> list:
        """Get list of available provider names.
        
        Returns:
            List of provider names
        """
        return list(cls.AVAILABLE_PROVIDERS.keys())

    def __repr__(self) -> str:
        return (
            f"WindowsUseAgent(provider={self.provider.get_provider_name()}, "
            f"model={self.provider.get_model_name()})"
        )
