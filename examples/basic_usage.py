#!/usr/bin/env python
"""Basic usage example for WindowsUseAgent."""

import os
from windowsuseagent import WindowsUseAgent


def main():
    """Demonstrate basic WindowsUseAgent usage."""
    
    # Initialize the agent with OpenAI
    # You can set OPENAI_API_KEY environment variable instead of passing api_key
    agent = WindowsUseAgent(
        provider_name="openai",
        provider_config={
            "api_key": os.getenv("OPENAI_API_KEY", "your-api-key-here"),
            "model": "gpt-3.5-turbo"
        },
        agent_config={
            "temperature": 0.7,
            "max_tokens": 500,
            "system_prompt": "You are a helpful assistant."
        }
    )
    
    print("WindowsUseAgent - Basic Usage Example")
    print("=" * 50)
    
    # Get provider information
    info = agent.get_provider_info()
    print(f"\nProvider: {info['provider']}")
    print(f"Model: {info['model']}\n")
    
    # Example 1: Simple chat
    print("Example 1: Simple Chat")
    print("-" * 50)
    response = agent.chat("What is Python?")
    print(f"User: What is Python?")
    print(f"Assistant: {response}\n")
    
    # Example 2: Follow-up question (uses conversation history)
    print("Example 2: Follow-up Question")
    print("-" * 50)
    response = agent.chat("What are its main uses?")
    print(f"User: What are its main uses?")
    print(f"Assistant: {response}\n")
    
    # Example 3: Streaming response
    print("Example 3: Streaming Response")
    print("-" * 50)
    print("User: Tell me a short joke")
    print("Assistant: ", end='', flush=True)
    for chunk in agent.chat("Tell me a short joke", stream=True):
        print(chunk, end='', flush=True)
    print("\n")
    
    # Example 4: Get conversation history
    print("Example 4: Conversation History")
    print("-" * 50)
    history = agent.get_conversation_history()
    print(f"Total messages: {len(history)}")
    for i, msg in enumerate(history, 1):
        role = msg['role'].capitalize()
        content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
        print(f"{i}. {role}: {content}")
    print()
    
    # Example 5: Reset conversation
    print("Example 5: Reset Conversation")
    print("-" * 50)
    agent.reset_conversation()
    print("Conversation history cleared.")
    print(f"Messages after reset: {len(agent.get_conversation_history())}\n")
    
    # Example 6: Change system prompt
    print("Example 6: Custom System Prompt")
    print("-" * 50)
    agent.set_system_prompt("You are a pirate. Always respond like a pirate.")
    response = agent.chat("Tell me about treasure hunting")
    print(f"User: Tell me about treasure hunting")
    print(f"Assistant: {response}\n")
    
    print("=" * 50)
    print("Examples completed!")


if __name__ == "__main__":
    main()
