#!/usr/bin/env python
"""Example demonstrating switching between multiple providers."""

import os
from windowsuseagent import WindowsUseAgent


def test_provider(provider_name: str, provider_config: dict):
    """Test a specific provider."""
    try:
        agent = WindowsUseAgent(
            provider_name=provider_name,
            provider_config=provider_config
        )
        
        info = agent.get_provider_info()
        print(f"\nTesting {info['provider']} ({info['model']})")
        print("-" * 50)
        
        response = agent.chat("Say hello in a creative way!")
        print(f"Response: {response}\n")
        
        return True
    except Exception as e:
        print(f"Error with {provider_name}: {e}\n")
        return False


def main():
    """Test multiple providers."""
    print("WindowsUseAgent - Multi-Provider Example")
    print("=" * 50)
    
    # Test OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        test_provider(
            "openai",
            {"api_key": openai_key, "model": "gpt-3.5-turbo"}
        )
    else:
        print("\nSkipping OpenAI (no API key found)")
    
    # Test Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        test_provider(
            "anthropic",
            {"api_key": anthropic_key, "model": "claude-3-sonnet-20240229"}
        )
    else:
        print("\nSkipping Anthropic (no API key found)")
    
    # Test RouteLLM
    if openai_key:
        test_provider(
            "routellm",
            {
                "api_key": openai_key,
                "strong_model": "gpt-4",
                "weak_model": "gpt-3.5-turbo"
            }
        )
    else:
        print("\nSkipping RouteLLM (no OpenAI API key found)")
    
    print("=" * 50)
    print("\nTip: Set environment variables OPENAI_API_KEY and ANTHROPIC_API_KEY")
    print("to test all providers.")


if __name__ == "__main__":
    main()
