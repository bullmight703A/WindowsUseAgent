"""Base LLM Provider interface for WindowsUseAgent."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers.
    
    This defines the common interface that all LLM providers must implement,
    ensuring consistency and easy swapping between different providers.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the provider with configuration.
        
        Args:
            config: Dictionary containing provider-specific configuration
                   including API keys, model names, and other settings.
        """
        self.config = config
        self.validate_config()

    @abstractmethod
    def validate_config(self) -> None:
        """Validate that required configuration parameters are present.
        
        Raises:
            ValueError: If required configuration is missing or invalid.
        """
        pass

    @abstractmethod
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Generate a response from the LLM.
        
        Args:
            prompt: The user's input prompt
            system_prompt: Optional system prompt to guide the LLM's behavior
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text response from the LLM
            
        Raises:
            Exception: If the API call fails
        """
        pass

    @abstractmethod
    def generate_streaming_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """Generate a streaming response from the LLM.
        
        Args:
            prompt: The user's input prompt
            system_prompt: Optional system prompt to guide the LLM's behavior
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Yields:
            Chunks of generated text as they become available
            
        Raises:
            Exception: If the API call fails
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the name of the currently configured model.
        
        Returns:
            Model name string
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of this provider.
        
        Returns:
            Provider name string
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.get_model_name()})"
