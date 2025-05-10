from unittest.mock import patch

import pytest
from src.starter.hello import hello_world


@patch("builtins.print")
def test_hello_world_mocked(mock_print):
    # Test with default argument
    hello_world()
    mock_print.assert_called_once_with("Hello, world!")

    # Reset mock for the next call
    mock_print.reset_mock()

    # Test with custom argument
    hello_world("Alice")
    mock_print.assert_called_once_with("Hello, Alice!")


@pytest.mark.integration
def test_hello_world_integration(capsys):
    # Test with default argument
    hello_world()
    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"

    # Test with custom argument
    hello_world("Alice")
    captured = capsys.readouterr()
    assert captured.out == "Hello, Alice!\n"
