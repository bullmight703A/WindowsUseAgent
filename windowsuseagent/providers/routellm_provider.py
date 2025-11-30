"""RouteLLM Provider implementation."""

import os
from typing import Optional, Dict, Any
from windowsuseagent.providers.base import BaseLLMProvider

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class RouteLLMProvider(BaseLLMProvider):
    """RouteLLM provider implementation.
    
    RouteLLM intelligently routes requests between different models based on
    query complexity, optimizing for cost and performance.
    
    For Phase 1, this uses OpenAI's API with a router configuration.
    Future phases can integrate with actual RouteLLM routing logic.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize RouteLLM provider.
        
        Args:
            config: Configuration dictionary with keys:
                - api_key: OpenAI API key for routing (or use OPENAI_API_KEY env var)
                - strong_model: Model for complex queries (default: gpt-4)
                - weak_model: Model for simple queries (default: gpt-3.5-turbo)
                - router_model: Model used for routing decisions (default: gpt-3.5-turbo)
                - threshold: Complexity threshold for routing (default: 0.5)
        """
        super().__init__(config)
        
        if OpenAI is None:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )
        
        api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
        
        self.client = OpenAI(api_key=api_key)
        self.strong_model = self.config.get("strong_model", "gpt-4")
        self.weak_model = self.config.get("weak_model", "gpt-3.5-turbo")
        self.router_model = self.config.get("router_model", "gpt-3.5-turbo")
        self.threshold = self.config.get("threshold", 0.5)

    def validate_config(self) -> None:
        """Validate RouteLLM configuration."""
        api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found for RouteLLM. Set 'api_key' in config or "
                "OPENAI_API_KEY environment variable."
            )

    def _route_query(self, prompt: str) -> str:
        """Determine which model to use based on query complexity.
        
        Args:
            prompt: User input prompt
            
        Returns:
            Model name to use (strong_model or weak_model)
        """
        # Simple heuristic-based routing for Phase 1
        # Future phases can integrate ML-based routing
        
        complexity_indicators = [
            "analyze", "complex", "detailed", "comprehensive", "explain",
            "compare", "evaluate", "critique", "reasoning", "why",
            "how does", "multi-step", "calculate", "solve"
        ]
        
        prompt_lower = prompt.lower()
        complexity_score = sum(
            1 for indicator in complexity_indicators 
            if indicator in prompt_lower
        ) / len(complexity_indicators)
        
        # Long prompts are often more complex
        if len(prompt) > 500:
            complexity_score += 0.2
        
        return self.strong_model if complexity_score > self.threshold else self.weak_model

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Generate a response using RouteLLM.
        
        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            Generated response text
        """
        # Route the query
        selected_model = self._route_query(prompt)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=selected_model,
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
        """Generate a streaming response using RouteLLM.
        
        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Yields:
            Chunks of generated text
        """
        # Route the query
        selected_model = self._route_query(prompt)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        stream = self.client.chat.completions.create(
            model=selected_model,
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
        """Get the RouteLLM model configuration."""
        return f"RouteLLM({self.weak_model}/{self.strong_model})"

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "RouteLLM"
