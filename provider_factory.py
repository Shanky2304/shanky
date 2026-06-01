
from llm_client import LLMClient, GroqClient, CerebrasClient

PROVIDER_MAP: dict[str, LLMClient] = {
    "cerebras": CerebrasClient,
    "groq": GroqClient,
}

_CLIENT_CACHE: dict[str, LLMClient] = {}

def make_client(provider: str) -> LLMClient:
    if provider not in _CLIENT_CACHE:
        # Create and add clients
        match provider:
            case "cerebras":
                _CLIENT_CACHE[provider] = CerebrasClient()

            case "groq":
                _CLIENT_CACHE[provider] = GroqClient()

            case _:
                raise ValueError(f"Unknown provider: {provider}")
    
    return _CLIENT_CACHE[provider]        