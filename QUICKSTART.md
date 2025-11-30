# WindowsUseAgent - Quick Start Guide

## Installation (Windows)

### One-Click Setup

Simply double-click one of these files:
- **`setup.bat`** - For Command Prompt
- **`install.ps1`** - For PowerShell (recommended)

The script will:
1. Check Python installation
2. Create a virtual environment
3. Install all dependencies
4. Set everything up automatically

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install
pip install -e .
```

## Quick Usage

### 1. Generate Configuration

```bash
windowsuseagent --generate-config
```

This creates a `config.json` file.

### 2. Add Your API Key

Edit `config.json` and add your API key:

```json
{
  "provider": "openai",
  "provider_config": {
    "api_key": "sk-your-actual-key-here",
    "model": "gpt-3.5-turbo"
  }
}
```

**Where to get API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

### 3. Run the Agent

```bash
# Interactive mode
windowsuseagent --config config.json

# Single query
windowsuseagent --config config.json --query "Hello, how are you?"

# With streaming
windowsuseagent --config config.json --stream
```

## Available Providers

### OpenAI (GPT)
```bash
windowsuseagent --provider openai --api-key YOUR_KEY --model gpt-3.5-turbo
```

### Anthropic (Claude)
```bash
windowsuseagent --provider anthropic --api-key YOUR_KEY --model claude-3-sonnet-20240229
```

### RouteLLM (Smart Routing)
```bash
windowsuseagent --provider routellm --api-key YOUR_OPENAI_KEY
```

## Python API Example

```python
from windowsuseagent import WindowsUseAgent

# Initialize
agent = WindowsUseAgent(
    provider_name="openai",
    provider_config={"api_key": "your-key", "model": "gpt-3.5-turbo"}
)

# Chat
response = agent.chat("Tell me a joke")
print(response)

# Stream
for chunk in agent.chat("Tell me a story", stream=True):
    print(chunk, end='', flush=True)
```

## Common Commands

```bash
# List available providers
windowsuseagent --list-providers

# Show version
windowsuseagent --version

# Help
windowsuseagent --help

# Generate config with specific provider
windowsuseagent --generate-config --provider anthropic --output my_config.json
```

## Troubleshooting

### Python not found
Install Python 3.8+ from https://www.python.org/downloads/
Make sure to check "Add Python to PATH" during installation.

### API key errors
- Make sure your API key is correct
- Check that you have credits in your account
- Verify the key starts with the right prefix:
  - OpenAI: `sk-...`
  - Anthropic: `sk-ant-...`

### Import errors
```bash
# Make sure you're in the virtual environment
venv\Scripts\activate

# Reinstall dependencies
pip install -e .
```

## Next Steps

- Check `examples/` folder for more examples
- Read the full [README.md](README.md) for detailed documentation
- Explore different providers and models
- Customize the system prompt for your use case

## Getting Help

- **Documentation**: See [README.md](README.md)
- **Examples**: Check the `examples/` directory
- **Issues**: Report bugs on GitHub
- **API Docs**: Check provider documentation:
  - [OpenAI Docs](https://platform.openai.com/docs)
  - [Anthropic Docs](https://docs.anthropic.com)

---

**Ready to get started?** Run `setup.bat` or `install.ps1` now!
