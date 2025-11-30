"""Command-line interface for WindowsUseAgent."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from windowsuseagent import WindowsUseAgent
from windowsuseagent.config import ConfigManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="WindowsUseAgent - A Windows Desktop Agent with Modular LLM Providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive chat with OpenAI
  windowsuseagent --provider openai --api-key YOUR_KEY
  
  # Use configuration file
  windowsuseagent --config config.json
  
  # Single query mode
  windowsuseagent --provider anthropic --query "What is the weather?"
  
  # Generate default configuration
  windowsuseagent --generate-config --output config.json
        """
    )
    
    # Configuration options
    config_group = parser.add_argument_group('Configuration')
    config_group.add_argument(
        '--config', '-c',
        type=str,
        help='Path to configuration file (JSON or YAML)'
    )
    config_group.add_argument(
        '--generate-config',
        action='store_true',
        help='Generate a default configuration file'
    )
    config_group.add_argument(
        '--output', '-o',
        type=str,
        default='config.json',
        help='Output path for generated configuration (default: config.json)'
    )
    
    # Provider options
    provider_group = parser.add_argument_group('Provider Settings')
    provider_group.add_argument(
        '--provider', '-p',
        type=str,
        choices=['openai', 'anthropic', 'routellm'],
        help='LLM provider to use'
    )
    provider_group.add_argument(
        '--model', '-m',
        type=str,
        help='Model name to use'
    )
    provider_group.add_argument(
        '--api-key', '-k',
        type=str,
        help='API key for the provider'
    )
    
    # Agent options
    agent_group = parser.add_argument_group('Agent Settings')
    agent_group.add_argument(
        '--temperature', '-t',
        type=float,
        help='Sampling temperature (0.0 to 1.0)'
    )
    agent_group.add_argument(
        '--max-tokens',
        type=int,
        help='Maximum tokens to generate'
    )
    agent_group.add_argument(
        '--system-prompt',
        type=str,
        help='Custom system prompt'
    )
    
    # Interaction options
    interaction_group = parser.add_argument_group('Interaction Mode')
    interaction_group.add_argument(
        '--query', '-q',
        type=str,
        help='Single query mode (non-interactive)'
    )
    interaction_group.add_argument(
        '--stream',
        action='store_true',
        help='Enable streaming responses'
    )
    
    # Other options
    parser.add_argument(
        '--list-providers',
        action='store_true',
        help='List available providers and exit'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )
    
    return parser.parse_args()


def setup_logging(verbose: bool) -> None:
    """Configure logging level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.getLogger().setLevel(level)


def generate_config(output_path: str, provider: str = "openai") -> None:
    """Generate a default configuration file."""
    try:
        format = "yaml" if output_path.endswith(('.yaml', '.yml')) else "json"
        ConfigManager.create_default_config(output_path, format, provider)
        print(f"✓ Configuration file generated: {output_path}")
        print(f"\nPlease edit the file to add your API keys and customize settings.")
    except Exception as e:
        logger.error(f"Failed to generate configuration: {e}")
        sys.exit(1)


def load_configuration(args) -> dict:
    """Load and merge configuration from file and command-line arguments."""
    config = {}
    
    # Load from file if specified
    if args.config:
        try:
            config = ConfigManager.load_config(args.config)
            logger.info(f"Loaded configuration from {args.config}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)
    
    # Override with command-line arguments
    if args.provider:
        config['provider'] = args.provider
    
    if 'provider_config' not in config:
        config['provider_config'] = {}
    
    if args.api_key:
        config['provider_config']['api_key'] = args.api_key
    if args.model:
        config['provider_config']['model'] = args.model
    
    if 'agent_config' not in config:
        config['agent_config'] = {}
    
    if args.temperature is not None:
        config['agent_config']['temperature'] = args.temperature
    if args.max_tokens is not None:
        config['agent_config']['max_tokens'] = args.max_tokens
    if args.system_prompt:
        config['agent_config']['system_prompt'] = args.system_prompt
    
    # Validate configuration
    if not config.get('provider'):
        logger.error("No provider specified. Use --provider or --config")
        sys.exit(1)
    
    return config


def interactive_chat(agent: WindowsUseAgent, stream: bool = False) -> None:
    """Run interactive chat session."""
    print("\n" + "="*60)
    print("WindowsUseAgent - Interactive Chat")
    print("="*60)
    provider_info = agent.get_provider_info()
    print(f"Provider: {provider_info['provider']}")
    print(f"Model: {provider_info['model']}")
    print("\nType 'exit', 'quit', or 'q' to exit")
    print("Type 'reset' to clear conversation history")
    print("Type 'help' for more commands")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            elif user_input.lower() == 'reset':
                agent.reset_conversation()
                print("\n✓ Conversation history cleared\n")
                continue
            elif user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  exit, quit, q  - Exit the chat")
                print("  reset          - Clear conversation history")
                print("  help           - Show this help message\n")
                continue
            
            # Get response
            print("\nAssistant: ", end='', flush=True)
            
            if stream:
                for chunk in agent.chat(user_input, stream=True):
                    print(chunk, end='', flush=True)
                print("\n")
            else:
                response = agent.chat(user_input)
                print(f"{response}\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\nError: {e}\n")


def single_query(agent: WindowsUseAgent, query: str, stream: bool = False) -> None:
    """Execute a single query and exit."""
    try:
        if stream:
            for chunk in agent.chat(query, stream=True):
                print(chunk, end='', flush=True)
            print()
        else:
            response = agent.chat(query)
            print(response)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Handle version
    if args.version:
        from windowsuseagent import __version__
        print(f"WindowsUseAgent v{__version__}")
        sys.exit(0)
    
    # Handle list providers
    if args.list_providers:
        print("\nAvailable providers:")
        for provider in WindowsUseAgent.list_providers():
            print(f"  - {provider}")
        print()
        sys.exit(0)
    
    # Handle config generation
    if args.generate_config:
        generate_config(args.output, args.provider or "openai")
        sys.exit(0)
    
    # Load configuration
    config = load_configuration(args)
    
    try:
        # Initialize agent
        agent = WindowsUseAgent(
            provider_name=config['provider'],
            provider_config=config['provider_config'],
            agent_config=config.get('agent_config', {})
        )
        
        # Run in appropriate mode
        if args.query:
            single_query(agent, args.query, args.stream)
        else:
            interactive_chat(agent, args.stream)
    
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
