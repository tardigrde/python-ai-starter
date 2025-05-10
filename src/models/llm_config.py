from pydantic import BaseModel


class LLMConfig(BaseModel):
    """Configuration for a vision model."""

    name: str
    provider: str
    api_key_env: str = "OPENROUTER_API_KEY"
    endpoint: str = "https://openrouter.ai/api/v1/chat/completions"
    max_tokens: int = 20000
    temperature: float = 0.1
