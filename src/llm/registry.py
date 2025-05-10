from typing import ClassVar

from src.models.llm_config import LLMConfig


class LLMRegistry:
    """Registry for LLM configurations."""

    MODELS: ClassVar[dict[str, LLMConfig]] = {
        "gemini-2.5-pro": LLMConfig(
            name="google/gemini-2.5-pro-preview-03-25",
            provider="google",
        ),
        # Best for image processing
        "gpt-4.1": LLMConfig(
            name="openai/gpt-4.1",
            provider="openai",
        ),
        # Cheapest for image processing
        "gpt-4.1-mini": LLMConfig(
            name="openai/gpt-4.1-mini",
            provider="openai",
        ),
        # Best value and fastest for large text processing
        "gemini-flash-2.5": LLMConfig(
            name="google/gemini-2.5-flash-preview",
            provider="google",
        ),
        "gemini-flash-2.5-thinking": LLMConfig(
            name="google/gemini-2.5-flash-preview:thinking",
            provider="google",
        ),
        # Add more models here as needed
    }

    @classmethod
    def get_model_config(cls, model_name: str) -> LLMConfig:
        """Get configuration for a specific LLM model.

        Args:
            model_name: Name of the model to get configuration for

        Returns:
            LLMConfig for the specified model

        Raises:
            ValueError: If model name is not found in available models
        """
        if model_name not in cls.MODELS:
            all_models = list(cls.MODELS.keys())
            raise ValueError(
                f"Model {model_name} not found. Available models: {all_models}"
            )
        return cls.MODELS[model_name]

    @classmethod
    def get_available_models(cls) -> list[str]:
        """Get list of available LLM models.

        Returns:
            List of available model names
        """
        return list(cls.MODELS.keys())
