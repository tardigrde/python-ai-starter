import pytest
import os
from unittest.mock import patch, MagicMock

from src.llm.service import LLMService
from src.models.llm_config import LLMConfig

import requests


@pytest.fixture
def mock_llm_config():
    """Fixture to provide a mock LLMConfig object."""
    return LLMConfig(
        name="test-model",
        provider="test-provider",
        endpoint="http://mock-endpoint.com",
        api_key_env="MOCK_API_KEY",
        max_tokens=100,
        temperature=0.5,
    )


@pytest.fixture
def llm_service():
    """Fixture to provide an LLMService instance."""
    return LLMService()


@patch("src.llm.registry.LLMRegistry.get_model_config")
@patch("os.getenv")
@patch("requests.post")
def test_send_llm_request_success(
    mock_post, mock_getenv, mock_get_model_config, llm_service, mock_llm_config
):
    """Test successful LLM request."""
    mock_get_model_config.return_value = mock_llm_config
    mock_getenv.return_value = "mock_api_key_value"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Generated response."}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "cost": 0.001},
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    messages = [{"role": "user", "content": "Hello"}]
    response_content = llm_service.send_llm_request("test-model", messages)

    mock_get_model_config.assert_called_once_with("test-model")
    mock_getenv.assert_called_once_with("MOCK_API_KEY")
    mock_post.assert_called_once_with(
        "http://mock-endpoint.com",
        headers={
            "Authorization": "Bearer mock_api_key_value",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/tardigrde/pyhton-ai-starter",
            "X-Title": "AI Starter",
        },
        json={
            "model": "test-model",
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0.5,
            "stream": False,
            "transforms": ["middle-out"],
            "route": "fallback",
            "handle_rate_limits": True,
            "usage": {"include": True},
        },
        timeout=60,
    )
    assert response_content == "Generated response."


@patch("src.llm.registry.LLMRegistry.get_model_config")
def test_send_llm_request_invalid_model(mock_get_model_config, llm_service):
    """Test LLM request with an invalid model name."""
    mock_get_model_config.side_effect = ValueError("Model not found")

    messages = [{"role": "user", "content": "Hello"}]
    response_content = llm_service.send_llm_request("invalid-model", messages)

    mock_get_model_config.assert_called_once_with("invalid-model")
    assert response_content is None


@patch("src.llm.registry.LLMRegistry.get_model_config")
@patch("os.getenv")
@patch("requests.post")
def test_send_llm_request_http_error(
    mock_post, mock_getenv, mock_get_model_config, llm_service, mock_llm_config
):
    """Test LLM request encountering an HTTP error."""
    mock_get_model_config.return_value = mock_llm_config
    mock_getenv.return_value = "mock_api_key_value"

    mock_post.side_effect = requests.exceptions.RequestException("HTTP Error")

    messages = [{"role": "user", "content": "Hello"}]
    response_content = llm_service.send_llm_request("test-model", messages)

    mock_get_model_config.assert_called_once_with("test-model")
    mock_getenv.assert_called_once_with("MOCK_API_KEY")
    mock_post.assert_called_once()  # Check if post was called
    assert response_content is None


@patch("src.llm.registry.LLMRegistry.get_model_config")
@patch("os.getenv")
@patch("requests.post")
def test_send_llm_request_unexpected_error(
    mock_post, mock_getenv, mock_get_model_config, llm_service, mock_llm_config
):
    """Test LLM request encountering an unexpected error."""
    mock_get_model_config.return_value = mock_llm_config
    mock_getenv.return_value = "mock_api_key_value"

    mock_post.side_effect = Exception("Unexpected error")

    messages = [{"role": "user", "content": "Hello"}]
    response_content = llm_service.send_llm_request("test-model", messages)

    mock_get_model_config.assert_called_once_with("test-model")
    mock_getenv.assert_called_once_with("MOCK_API_KEY")
    mock_post.assert_called_once()  # Check if post was called
    assert response_content is None


@patch("src.llm.registry.LLMRegistry.get_model_config")
@patch("os.getenv")
@patch("requests.post")
def test_send_llm_request_no_content_in_response(
    mock_post, mock_getenv, mock_get_model_config, llm_service, mock_llm_config
):
    """Test LLM request where the response JSON does not contain content."""
    mock_get_model_config.return_value = mock_llm_config
    mock_getenv.return_value = "mock_api_key_value"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "some_other_key": "value",
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "cost": 0.001},
    }  # No 'choices', 'content', or 'text'
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    messages = [{"role": "user", "content": "Hello"}]
    response_content = llm_service.send_llm_request("test-model", messages)

    mock_get_model_config.assert_called_once_with("test-model")
    mock_getenv.assert_called_once_with("MOCK_API_KEY")
    mock_post.assert_called_once()  # Check if post was called
    assert response_content is None


def test__get_llm_headers(llm_service):
    """Test the _get_llm_headers helper method."""
    with patch("os.getenv", return_value="dummy_api_key"):
        headers = llm_service._get_llm_headers("DUMMY_API_KEY_ENV")
        assert headers == {
            "Authorization": "Bearer dummy_api_key",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/tardigrde/pyhton-ai-starter",
            "X-Title": "AI Starter",
        }
        os.getenv.assert_called_once_with("DUMMY_API_KEY_ENV")


def test__prepare_llm_payload(llm_service, mock_llm_config):
    """Test the _prepare_llm_payload helper method."""
    messages = [{"role": "user", "content": "Test message"}]
    payload = llm_service._prepare_llm_payload(mock_llm_config, messages)
    assert payload == {
        "model": "test-model",
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0.5,
        "stream": False,
        "transforms": ["middle-out"],
        "route": "fallback",
        "handle_rate_limits": True,
        "usage": {"include": True},
    }


def test__extract_content_from_response_choices(llm_service):
    """Test _extract_content_from_response with 'choices' structure."""
    response_json = {"choices": [{"message": {"content": "Content from choices"}}]}
    content = llm_service._extract_content_from_response(response_json)
    assert content == "Content from choices"


def test__extract_content_from_response_content_key(llm_service):
    """Test _extract_content_from_response with 'content' key."""
    response_json = {"content": "Content from content key"}
    content = llm_service._extract_content_from_response(response_json)
    assert content == "Content from content key"


def test__extract_content_from_response_text_key(llm_service):
    """Test _extract_content_from_response with 'text' key."""
    response_json = {"text": "Content from text key"}
    content = llm_service._extract_content_from_response(response_json)
    assert content == "Content from text key"


def test__extract_content_from_response_no_content(llm_service):
    """Test _extract_content_from_response with no content keys."""
    response_json = {"some_key": "some_value"}
    content = llm_service._extract_content_from_response(response_json)
    assert content is None
