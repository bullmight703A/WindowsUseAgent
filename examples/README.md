# WindowsUseAgent Examples

This directory contains example configurations and scripts to help you get started with WindowsUseAgent.

## Configuration Examples

### JSON Configurations

- **`config_openai.json`** - OpenAI (GPT) configuration
- **`config_anthropic.json`** - Anthropic (Claude) configuration
- **`config_routellm.json`** - RouteLLM configuration

### YAML Configuration

- **`config_example.yaml`** - Example YAML configuration

## Python Examples

### `basic_usage.py`

Demonstrates fundamental WindowsUseAgent features:
- Initializing the agent
- Simple chat interactions
- Streaming responses
- Conversation history
- Resetting conversations
- Custom system prompts

**Run:**
```bash
python basic_usage.py
```

### `multi_provider_example.py`

Shows how to switch between different LLM providers:
- Testing OpenAI provider
- Testing Anthropic provider
- Testing RouteLLM provider

**Run:**
```bash
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
python multi_provider_example.py
```

## Using the Examples

1. **Set up your environment:**
   ```bash
   # Install WindowsUseAgent
   pip install -e ..
   
   # Set your API keys
   export OPENAI_API_KEY="your-openai-key"
   export ANTHROPIC_API_KEY="your-anthropic-key"
   ```

2. **Run CLI with example config:**
   ```bash
   # Edit the config file first to add your API key
   windowsuseagent --config examples/config_openai.json
   ```

3. **Run Python examples:**
   ```bash
   python examples/basic_usage.py
   python examples/multi_provider_example.py
   ```

## Creating Your Own Examples

Use these examples as templates for your own applications:

1. Copy an example file
2. Modify the configuration and logic
3. Add your custom functionality

## Tips

- **Security**: Never commit API keys to version control
- **Environment Variables**: Use `.env` files or system environment variables for sensitive data
- **Configuration Files**: Keep config files outside version control (they're in `.gitignore`)
- **Error Handling**: Always wrap API calls in try-except blocks for production use

## Need Help?

Check the main [README.md](../README.md) for more detailed documentation and usage instructions.
