"""Tests for the core WindowsUseAgent."""

import pytest
from windowsuseagent import WindowsUseAgent
from windowsuseagent.providers.base import BaseLLMProvider


class MockProvider(BaseLLMProvider):
    """Mock provider for testing."""
    
    def validate_config(self):
        pass
    
    def generate_response(self, prompt, system_prompt=None, temperature=0.7, max_tokens=1000, **kwargs):
        return f"Mock response to: {prompt}"
    
    def generate_streaming_response(self, prompt, system_prompt=None, temperature=0.7, max_tokens=1000, **kwargs):
        words = f"Mock streaming response to: {prompt}".split()
        for word in words:
            yield word + " "
    
    def get_model_name(self):
        return "mock-model"
    
    def get_provider_name(self):
        return "MockProvider"


class TestWindowsUseAgent:
    """Test cases for WindowsUseAgent."""
    
    def setup_method(self):
        """Set up test fixtures."""
        WindowsUseAgent.register_provider("mock", MockProvider)
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = WindowsUseAgent(
            provider_name="mock",
            provider_config={}
        )
        assert agent is not None
        assert agent.provider_name == "mock"
    
    def test_invalid_provider(self):
        """Test initialization with invalid provider."""
        with pytest.raises(ValueError):
            WindowsUseAgent(
                provider_name="invalid_provider",
                provider_config={}
            )
    
    def test_chat(self):
        """Test basic chat functionality."""
        agent = WindowsUseAgent(
            provider_name="mock",
            provider_config={}
        )
        response = agent.chat("Hello")
        assert "Mock response" in response
        assert "Hello" in response
    
    def test_streaming_chat(self):
        """Test streaming chat functionality."""
        agent = WindowsUseAgent(
            provider_name="mock",
            provider_config={}
        )
        chunks = list(agent.chat("Hello", stream=True))
        assert len(chunks) > 0
        full_response = "".join(chunks)
        assert "Mock streaming" in full_response
    
    def test_conversation_history(self):
        """Test conversation history tracking."""
        agent = WindowsUseAgent(
            provider_name="mock",
            provider_config={}
        )
        agent.chat("First message")
        agent.chat("Second message")
        
        history = agent.get_conversation_history()
        assert len(history) == 4  # 2 user + 2 assistant messages
    
    def test_reset_conversation(self):
        """Test conversation reset."""
        agent = WindowsUseAgent(
            provider_name="mock",
            provider_config={}
        )
        agent.chat("Test message")
        assert len(agent.get_conversation_history()) > 0
        
        agent.reset_conversation()
        assert len(agent.get_conversation_history()) == 0
    
    def test_set_system_prompt(self):
        """Test system prompt update."""
        agent = WindowsUseAgent(
            provider_name="mock",
            provider_config={}
        )
        new_prompt = "You are a test assistant."
        agent.set_system_prompt(new_prompt)
        assert agent.system_prompt == new_prompt
    
    def test_get_provider_info(self):
        """Test getting provider information."""
        agent = WindowsUseAgent(
            provider_name="mock",
            provider_config={}
        )
        info = agent.get_provider_info()
        assert "provider" in info
        assert "model" in info
        assert info["provider"] == "MockProvider"
        assert info["model"] == "mock-model"
    
    def test_list_providers(self):
        """Test listing available providers."""
        providers = WindowsUseAgent.list_providers()
        assert "mock" in providers
        assert "openai" in providers
        assert "anthropic" in providers
        assert "routellm" in providers
