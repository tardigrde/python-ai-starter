import pytest
from pydantic import ValidationError

from src.models.llm_config import LLMConfig
from src.llm.registry import LLMRegistry


def test_llm_config_valid():
    """Test creating a valid LLMConfig instance."""
    config_data = {
        "name": "test-model",
        "provider": "test-provider",
        "endpoint": "http://test-endpoint.com",
        "api_key_env": "TEST_API_KEY",
        "max_tokens": 100,
        "temperature": 0.7,
    }
    config = LLMConfig(**config_data)
    assert config.name == "test-model"
    assert config.provider == "test-provider"
    assert config.endpoint == "http://test-endpoint.com"
    assert config.api_key_env == "TEST_API_KEY"
    assert config.max_tokens == 100
    assert config.temperature == 0.7


def test_llm_config_missing_required_field():
    """Test creating LLMConfig with a missing required field (name)."""
    config_data = {
        "provider": "test-provider",
        "endpoint": "http://test-endpoint.com",
        "api_key_env": "TEST_API_KEY",
    }
    with pytest.raises(ValidationError):
        LLMConfig(**config_data)


def test_llm_config_invalid_missing_provider():
    """Test creating LLMConfig with missing provider."""
    config_data = {
        "name": "test-model",
        "endpoint": "invalid-url",
        "api_key_env": "TEST_API_KEY",
    }
    with pytest.raises(ValidationError):
        LLMConfig(**config_data)


def test_llm_config_optional_fields_default():
    """Test creating LLMConfig with only required fields, checking defaults."""
    config_data = {
        "name": "test-model",
        "provider": "test-provider",
        "endpoint": "http://test-endpoint.com",
        "api_key_env": "TEST_API_KEY",
    }
    config = LLMConfig(**config_data)
    assert config.name == "test-model"
    assert config.provider == "test-provider"
    assert config.endpoint == "http://test-endpoint.com"
    assert config.api_key_env == "TEST_API_KEY"
    assert config.max_tokens == 20000
    assert config.temperature == 0.1
