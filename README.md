# WindowsUseAgent

A powerful Windows Desktop Agent with modular LLM provider architecture. Easily switch between OpenAI, Anthropic (Claude), RouteLLM, and other providers for building intelligent desktop automation and assistance tools.

## 🌟 Features

- **Modular LLM Provider Architecture**: Easily switch between different LLM providers
- **Three Built-in Providers**:
  - **OpenAI**: GPT-3.5, GPT-4, and other OpenAI models
  - **Anthropic**: Claude 2, Claude 3, and other Anthropic models
  - **RouteLLM**: Intelligent routing between models for cost optimization
- **Flexible Configuration**: JSON/YAML configuration files with environment variable support
- **Interactive CLI**: Feature-rich command-line interface with streaming support
- **Extensible Design**: Easy to add custom providers
- **Production Ready**: Well-documented, tested, and type-hinted code

## 📋 Requirements

- Python 3.8 or higher
- Windows, Linux, or macOS
- API keys for your chosen provider(s)

## 🚀 Quick Start

### Windows Installation

#### Option 1: Using setup.bat (Recommended)
```batch
# Clone the repository
git clone https://github.com/bullmight703A/WindowsUseAgent.git
cd WindowsUseAgent

# Run the setup script
setup.bat
```

#### Option 2: Using PowerShell
```powershell
# Clone the repository
git clone https://github.com/bullmight703A/WindowsUseAgent.git
cd WindowsUseAgent

# You may need to allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run the setup script
.\install.ps1
```

### Linux/macOS Installation

```bash
# Clone the repository
git clone https://github.com/bullmight703A/WindowsUseAgent.git
cd WindowsUseAgent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### Configuration

1. **Generate a configuration file:**
```bash
windowsuseagent --generate-config --output config.json
```

2. **Edit the configuration file** with your API keys:
```json
{
  "provider": "openai",
  "provider_config": {
    "model": "gpt-3.5-turbo",
    "api_key": "your-api-key-here"
  },
  "agent_config": {
    "temperature": 0.7,
    "max_tokens": 1000,
    "system_prompt": "You are a helpful Windows desktop assistant."
  }
}
```

3. **Alternative: Use environment variables**
```bash
# Set environment variables instead of storing in config file
export OPENAI_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## 💻 Usage

### Interactive Chat Mode

```bash
# Using configuration file
windowsuseagent --config config.json

# Using command-line arguments
windowsuseagent --provider openai --api-key YOUR_KEY

# With streaming responses
windowsuseagent --config config.json --stream
```

### Single Query Mode

```bash
# Execute a single query and exit
windowsuseagent --config config.json --query "What is the weather today?"

# With streaming
windowsuseagent --provider anthropic --api-key YOUR_KEY --query "Explain quantum computing" --stream
```

### Command-Line Options

```bash
windowsuseagent --help

Configuration:
  --config, -c          Path to configuration file (JSON or YAML)
  --generate-config     Generate a default configuration file
  --output, -o          Output path for generated configuration

Provider Settings:
  --provider, -p        LLM provider to use (openai, anthropic, routellm)
  --model, -m           Model name to use
  --api-key, -k         API key for the provider

Agent Settings:
  --temperature, -t     Sampling temperature (0.0 to 1.0)
  --max-tokens          Maximum tokens to generate
  --system-prompt       Custom system prompt

Interaction Mode:
  --query, -q           Single query mode (non-interactive)
  --stream              Enable streaming responses

Other:
  --list-providers      List available providers
  --verbose, -v         Enable verbose logging
  --version             Show version information
```

## 📚 Provider Configuration

### OpenAI

```json
{
  "provider": "openai",
  "provider_config": {
    "api_key": "sk-...",
    "model": "gpt-3.5-turbo",
    "organization": "org-..."  // Optional
  }
}
```

**Supported Models**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo-preview`, etc.

### Anthropic (Claude)

```json
{
  "provider": "anthropic",
  "provider_config": {
    "api_key": "sk-ant-...",
    "model": "claude-3-sonnet-20240229"
  }
}
```

**Supported Models**: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307`, etc.

### RouteLLM

```json
{
  "provider": "routellm",
  "provider_config": {
    "api_key": "sk-...",
    "strong_model": "gpt-4",
    "weak_model": "gpt-3.5-turbo",
    "threshold": 0.5
  }
}
```

RouteLLM intelligently routes requests between a strong model (for complex queries) and a weak model (for simple queries) to optimize for cost and performance.

## 🔧 Advanced Usage

### Python API

```python
from windowsuseagent import WindowsUseAgent

# Initialize the agent
agent = WindowsUseAgent(
    provider_name="openai",
    provider_config={
        "api_key": "your-api-key",
        "model": "gpt-3.5-turbo"
    },
    agent_config={
        "temperature": 0.7,
        "max_tokens": 1000,
        "system_prompt": "You are a helpful assistant."
    }
)

# Chat with the agent
response = agent.chat("Hello, how are you?")
print(response)

# Streaming response
for chunk in agent.chat("Tell me a story", stream=True):
    print(chunk, end='', flush=True)

# Reset conversation
agent.reset_conversation()

# Get provider info
info = agent.get_provider_info()
print(f"Using {info['provider']} with model {info['model']}")
```

### Custom Provider

Create your own LLM provider by inheriting from `BaseLLMProvider`:

```python
from windowsuseagent.providers.base import BaseLLMProvider

class MyCustomProvider(BaseLLMProvider):
    def validate_config(self):
        # Validate configuration
        pass
    
    def generate_response(self, prompt, system_prompt=None, temperature=0.7, max_tokens=1000, **kwargs):
        # Implement response generation
        pass
    
    def generate_streaming_response(self, prompt, system_prompt=None, temperature=0.7, max_tokens=1000, **kwargs):
        # Implement streaming response
        pass
    
    def get_model_name(self):
        return "my-custom-model"
    
    def get_provider_name(self):
        return "MyCustomProvider"

# Register the provider
from windowsuseagent import WindowsUseAgent
WindowsUseAgent.register_provider("custom", MyCustomProvider)

# Use your custom provider
agent = WindowsUseAgent(
    provider_name="custom",
    provider_config={...}
)
```

### Using YAML Configuration

```yaml
# config.yaml
provider: openai
provider_config:
  api_key: your-api-key
  model: gpt-3.5-turbo
agent_config:
  temperature: 0.7
  max_tokens: 1000
  system_prompt: You are a helpful Windows desktop assistant.
```

```bash
windowsuseagent --config config.yaml
```

### Environment Variables

The agent supports loading API keys from environment variables:

```bash
# .env file or environment
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## 📁 Project Structure

```
WindowsUseAgent/
├── windowsuseagent/          # Main package
│   ├── __init__.py           # Package initialization
│   ├── agent.py              # Core agent implementation
│   ├── providers/            # LLM provider implementations
│   │   ├── __init__.py
│   │   ├── base.py           # Base provider interface
│   │   ├── openai_provider.py
│   │   ├── anthropic_provider.py
│   │   └── routellm_provider.py
│   ├── config/               # Configuration management
│   │   ├── __init__.py
│   │   └── config_manager.py
│   └── cli/                  # Command-line interface
│       ├── __init__.py
│       └── main.py
├── tests/                    # Test suite
├── examples/                 # Example scripts
├── setup.py                  # Package setup
├── requirements.txt          # Dependencies
├── setup.bat                 # Windows setup script
├── install.ps1               # PowerShell setup script
├── .gitignore               # Git ignore rules
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## 🧪 Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run tests with coverage
pytest --cov=windowsuseagent tests/
```

### Code Formatting

```bash
# Format code with black
black windowsuseagent/

# Lint with flake8
flake8 windowsuseagent/

# Type checking with mypy
mypy windowsuseagent/
```

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core agent framework with modular architecture
- ✅ OpenAI, Anthropic, and RouteLLM providers
- ✅ CLI interface and configuration system
- ✅ Comprehensive documentation

### Phase 2 (Planned)
- 🔲 Windows desktop automation capabilities
- 🔲 Screen capture and vision capabilities
- 🔲 Mouse and keyboard control
- 🔲 Application interaction
- 🔲 GUI interface

### Phase 3 (Future)
- 🔲 Advanced RouteLLM with ML-based routing
- 🔲 Multi-modal support (vision, audio)
- 🔲 Task planning and execution
- 🔲 Memory and context management
- 🔲 Plugin system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for their powerful GPT models
- Anthropic for Claude
- The open-source community for various tools and libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/bullmight703A/WindowsUseAgent/issues)
- **Documentation**: See [examples/](examples/) folder for more examples
- **Discussions**: [GitHub Discussions](https://github.com/bullmight703A/WindowsUseAgent/discussions)

## 🔒 Security

Never commit your API keys to version control. Use:
- Configuration files (excluded by `.gitignore`)
- Environment variables
- Secure secret management solutions

---

**Made with ❤️ by the WindowsUseAgent Team**
