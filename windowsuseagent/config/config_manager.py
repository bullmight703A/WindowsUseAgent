"""Configuration management for WindowsUseAgent."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConfigManager:
    """Manages loading and saving configuration files.
    
    Supports both JSON and YAML formats.
    """

    DEFAULT_CONFIG = {
        "provider": "openai",
        "provider_config": {
            "model": "gpt-3.5-turbo",
            "api_key": ""
        },
        "agent_config": {
            "temperature": 0.7,
            "max_tokens": 1000,
            "system_prompt": "You are a helpful Windows desktop assistant."
        }
    }

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from a file.
        
        Args:
            config_path: Path to configuration file (.json or .yaml/.yml)
            
        Returns:
            Configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If file format is unsupported
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        suffix = config_path.suffix.lower()
        
        if suffix == ".json":
            return ConfigManager._load_json(config_path)
        elif suffix in [".yaml", ".yml"]:
            return ConfigManager._load_yaml(config_path)
        else:
            raise ValueError(
                f"Unsupported configuration format: {suffix}. "
                "Use .json, .yaml, or .yml"
            )

    @staticmethod
    def _load_json(config_path: Path) -> Dict[str, Any]:
        """Load JSON configuration file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def _load_yaml(config_path: Path) -> Dict[str, Any]:
        """Load YAML configuration file."""
        if not YAML_AVAILABLE:
            raise ImportError(
                "PyYAML not installed. Install with: pip install pyyaml"
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def save_config(
        config: Dict[str, Any],
        config_path: str,
        format: str = "json"
    ) -> None:
        """Save configuration to a file.
        
        Args:
            config: Configuration dictionary
            config_path: Path to save configuration file
            format: File format ('json' or 'yaml')
            
        Raises:
            ValueError: If format is unsupported
        """
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        format = format.lower()
        
        if format == "json":
            ConfigManager._save_json(config, config_path)
        elif format == "yaml":
            ConfigManager._save_yaml(config, config_path)
        else:
            raise ValueError(
                f"Unsupported format: {format}. Use 'json' or 'yaml'"
            )

    @staticmethod
    def _save_json(config: Dict[str, Any], config_path: Path) -> None:
        """Save configuration as JSON."""
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    @staticmethod
    def _save_yaml(config: Dict[str, Any], config_path: Path) -> None:
        """Save configuration as YAML."""
        if not YAML_AVAILABLE:
            raise ImportError(
                "PyYAML not installed. Install with: pip install pyyaml"
            )
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)

    @staticmethod
    def create_default_config(
        config_path: str,
        format: str = "json",
        provider: str = "openai"
    ) -> None:
        """Create a default configuration file.
        
        Args:
            config_path: Path to save configuration file
            format: File format ('json' or 'yaml')
            provider: Default provider to use
        """
        config = ConfigManager.DEFAULT_CONFIG.copy()
        config["provider"] = provider
        
        ConfigManager.save_config(config, config_path, format)

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration structure.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["provider", "provider_config"]
        
        for key in required_keys:
            if key not in config:
                return False
        
        return True

    @staticmethod
    def merge_configs(
        base_config: Dict[str, Any],
        override_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge two configurations, with override taking precedence.
        
        Args:
            base_config: Base configuration
            override_config: Configuration to override with
            
        Returns:
            Merged configuration
        """
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = ConfigManager.merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
