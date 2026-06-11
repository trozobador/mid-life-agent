import os
from dotenv import load_dotenv

load_dotenv()

_MODELS = {
    "openai":    "openai/gpt-4o",
    "anthropic": "anthropic/claude-sonnet-4-6",
    "gemini":    "gemini/gemini-2.5-flash",
    "grok":      "xai/grok-3-latest",
}

_API_KEY_ENV = {
    "openai":    "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini":    "GOOGLE_API_KEY",
    "grok":      "XAI_API_KEY",
}


def get_llm(provider: str = None, temperature: float = 0.4):
    """Returns a crewai.LLM instance for the given provider."""
    from crewai import LLM

    provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    model = _MODELS.get(provider)
    if not model:
        raise ValueError(
            f"Provider not supported: '{provider}'. "
            "Choose from: openai, anthropic, gemini, grok"
        )
    api_key = os.getenv(_API_KEY_ENV.get(provider, ""))
    kwargs = {"temperature": temperature}
    if api_key:
        kwargs["api_key"] = api_key
    return LLM(model=model, **kwargs)
