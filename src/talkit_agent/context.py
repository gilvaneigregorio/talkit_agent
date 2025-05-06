from dataclasses import dataclass

from .ai_models import AIModelClient
from .open_api import OpenAPIClient


@dataclass
class AgentContext:
    base_url: str
    headers: dict[str, str]
    open_api_client: OpenAPIClient
    ai_model_client: AIModelClient
