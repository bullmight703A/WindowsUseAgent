"""Anthropic (Claude) LLM Provider implementation."""

import os
from typing import Optional, Dict, Any
from windowsuseagent.providers.base import BaseLLMProvider

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider implementation.
    
    Supports Claude 2, Claude 3, and other Anthropic models.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize Anthropic provider.
        
        Args:
            config: Configuration dictionary with keys:
                - api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
                - model: Model name (default: claude-3-sonnet-20240229)
        """
        super().__init__(config)
        
        if Anthropic is None:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )
        
        api_key = self.config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        
        self.client = Anthropic(api_key=api_key)
        self.model = self.config.get("model", "claude-3-sonnet-20240229")

    def validate_config(self) -> None:
        """Validate Anthropic configuration."""
        api_key = self.config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "Anthropic API key not found. Set 'api_key' in config or "
                "ANTHROPIC_API_KEY environment variable."
            )

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Generate a response using Anthropic API.
        
        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Anthropic-specific parameters
            
        Returns:
            Generated response text
        """
        messages = [{"role": "user", "content": prompt}]
        
        request_params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        if system_prompt:
            request_params["system"] = system_prompt
        
        response = self.client.messages.create(**request_params)
        
        return response.content[0].text

    def generate_streaming_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """Generate a streaming response using Anthropic API.
        
        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Anthropic-specific parameters
            
        Yields:
            Chunks of generated text
        """
        messages = [{"role": "user", "content": prompt}]
        
        request_params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        if system_prompt:
            request_params["system"] = system_prompt
        
        with self.client.messages.stream(**request_params) as stream:
            for text in stream.text_stream:
                yield text

    def get_model_name(self) -> str:
        """Get the Anthropic model name."""
        return self.model

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "Anthropic"
