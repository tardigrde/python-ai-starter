import json
import os
from typing import Any

import requests

from src.llm.registry import LLMRegistry
from src.models.llm_config import LLMConfig
from src.utils.logging import setup_logging


class LLMService:
    """
    A service class for interacting with Language Model (LLM) APIs.

    This class provides methods for sending requests to LLMs, handling responses,
    and managing configuration.
    """

    logger = setup_logging("llm_service")

    def send_llm_request(
        self, model_name: str, messages: list[dict[str, Any]]
    ) -> str | None:
        """
        Sends a request to the LLM via OpenRouter.

        Args:
            model_name: The name of the LLM model to use.
            messages: The list of messages for the LLM.

        Returns:
            The content of the LLM's response, or None if an error occurred.
        """
        try:
            model_config: LLMConfig = LLMRegistry.get_model_config(model_name)
        except ValueError as e:
            self.logger.error(f"Invalid model name: {e}")
            return None

        headers = self._get_llm_headers(model_config.api_key_env)
        payload = self._prepare_llm_payload(model_config, messages)

        try:
            self.logger.info(
                f"API request with {model_name} to {model_config.endpoint}"
            )
            response = requests.post(
                model_config.endpoint,
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()

            response_json = response.json()

            # Log usage information if available
            if "usage" in response_json:
                usage = response_json["usage"]
                try:
                    usage_cost = float(usage.get("cost"))
                except Exception:
                    self.logger.error("Could not extract usage cost from response: ")
                self.logger.info(
                    f"LLM API call usage: prompt_tokens={usage.get('prompt_tokens')}, "
                    f"completion_tokens={usage.get('completion_tokens')}, "
                    f"cost=${usage_cost}"
                )

            content = self._extract_content_from_response(response_json)

            if not content:
                response_keys = list(response_json.keys())
                self.logger.error(
                    "Could not extract content from LLM response."
                    f"Response keys: {response_keys}"
                )
                if "choices" in response_json:
                    choices = json.dumps(response_json["choices"], indent=2)
                    self.logger.error(f"Choices structure: {choices}")
                return None
            return content

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending LLM request: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during LLM request: {e}")
            return None

    def _get_llm_headers(self, api_key_env: str) -> dict[str, str]:
        """
        Prepares the headers for the LLM API request.

        Args:
            api_key_env: The environment variable name containing the API key.

        Returns:
            A dictionary containing the request headers.
        """
        return {
            "Authorization": f"Bearer {os.getenv(api_key_env)}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/tardigrde/pyhton-ai-starter",
            "X-Title": "AI Starter",
        }

    def _prepare_llm_payload(
        self, model_config: LLMConfig, messages: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Prepares the payload for the LLM API request.

        Args:
            model_config: The configuration for the LLM model.
            messages: The list of messages for the LLM.

        Returns:
            A dictionary containing the request payload.
        """
        return {
            "model": model_config.name,
            "messages": messages,
            "max_tokens": model_config.max_tokens,
            "temperature": model_config.temperature,
            "stream": False,
            "transforms": ["middle-out"],
            "route": "fallback",
            "handle_rate_limits": True,
            "usage": {"include": True},
        }

    def _extract_content_from_response(self, response_json: dict) -> str | None:
        """
        Extracts the content string from the LLM API response.

        Args:
            response_json: The JSON response from the LLM API.

        Returns:
            The extracted content string, or None if not found.
        """
        content = None
        if response_json.get("choices"):
            if "message" in response_json["choices"][0]:
                content = response_json["choices"][0]["message"].get("content")
        elif "content" in response_json:
            content = response_json["content"]
        elif "text" in response_json:
            content = response_json["text"]
        return content
