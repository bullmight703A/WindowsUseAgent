"""Tests for ConfigManager."""

import json
import pytest
from pathlib import Path
from windowsuseagent.config import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""
    
    def test_load_json_config(self, tmp_path):
        """Test loading JSON configuration."""
        config_file = tmp_path / "config.json"
        config_data = {
            "provider": "openai",
            "provider_config": {"api_key": "test-key"}
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        loaded_config = ConfigManager.load_config(str(config_file))
        assert loaded_config == config_data
    
    def test_save_json_config(self, tmp_path):
        """Test saving JSON configuration."""
        config_file = tmp_path / "config.json"
        config_data = {
            "provider": "openai",
            "provider_config": {"api_key": "test-key"}
        }
        
        ConfigManager.save_config(config_data, str(config_file), format="json")
        
        with open(config_file, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data == config_data
    
    def test_validate_config(self):
        """Test configuration validation."""
        valid_config = {
            "provider": "openai",
            "provider_config": {"api_key": "test-key"}
        }
        assert ConfigManager.validate_config(valid_config) is True
        
        invalid_config = {"provider": "openai"}
        assert ConfigManager.validate_config(invalid_config) is False
    
    def test_merge_configs(self):
        """Test configuration merging."""
        base_config = {
            "provider": "openai",
            "provider_config": {"api_key": "base-key", "model": "gpt-3.5"}
        }
        override_config = {
            "provider_config": {"api_key": "override-key"}
        }
        
        merged = ConfigManager.merge_configs(base_config, override_config)
        
        assert merged["provider"] == "openai"
        assert merged["provider_config"]["api_key"] == "override-key"
        assert merged["provider_config"]["model"] == "gpt-3.5"
    
    def test_create_default_config(self, tmp_path):
        """Test creating default configuration."""
        config_file = tmp_path / "config.json"
        
        ConfigManager.create_default_config(str(config_file), format="json")
        
        assert config_file.exists()
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        assert "provider" in config
        assert "provider_config" in config
