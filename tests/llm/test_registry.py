import pytest
import os
import json  # Import json
from unittest.mock import patch

from src.llm.registry import LLMRegistry
from src.models.llm_config import LLMConfig


def test_get_available_models():
    """Test getting the list of available model names."""
    # Assuming LLMRegistry.MODELS is hardcoded as per src/llm/registry.py
    expected_models = list(LLMRegistry.MODELS.keys())
    available_models = LLMRegistry.get_available_models()
    assert available_models == expected_models


def test_get_model_config_success():
    """Test getting configuration for a valid model name."""
    # Assuming LLMRegistry.MODELS is hardcoded
    model_name = (
        "gemini-2.5-pro"  # Use a model name that exists in the actual MODELS dict
    )
    model_config = LLMRegistry.get_model_config(model_name)
    assert model_config.name == LLMRegistry.MODELS[model_name].name
    assert model_config.provider == LLMRegistry.MODELS[model_name].provider
    # Add assertions for other fields if they are present in the actual LLMConfig instances


def test_get_model_config_not_found():
    """Test getting configuration for a model name that does not exist."""
    non_existent_model = "non-existent-model"
    with pytest.raises(
        ValueError, match=f"Model {non_existent_model} not found. Available models: .*"
    ):
        LLMRegistry.get_model_config(non_existent_model)
