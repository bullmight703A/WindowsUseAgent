"""OpenAI LLM Provider implementation."""

import os
from typing import Optional, Dict, Any
from windowsuseagent.providers.base import BaseLLMProvider

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider implementation.
    
    Supports GPT-3.5, GPT-4, and other OpenAI models.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenAI provider.
        
        Args:
            config: Configuration dictionary with keys:
                - api_key: OpenAI API key (or use OPENAI_API_KEY env var)
                - model: Model name (default: gpt-3.5-turbo)
                - organization: Optional organization ID
        """
        super().__init__(config)
        
        if OpenAI is None:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )
        
        api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
        organization = self.config.get("organization")
        
        self.client = OpenAI(
            api_key=api_key,
            organization=organization
        )
        self.model = self.config.get("model", "gpt-3.5-turbo")

    def validate_config(self) -> None:
        """Validate OpenAI configuration."""
        api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Set 'api_key' in config or "
                "OPENAI_API_KEY environment variable."
            )

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Generate a response using OpenAI API.
        
        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            Generated response text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content

    def generate_streaming_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """Generate a streaming response using OpenAI API.
        
        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional OpenAI-specific parameters
            
        Yields:
            Chunks of generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def get_model_name(self) -> str:
        """Get the OpenAI model name."""
        return self.model

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "OpenAI"
