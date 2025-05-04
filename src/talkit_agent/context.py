from dataclasses import dataclass

from .models import GPTModel
from .open_api import OpenAPI


@dataclass
class AgentContext:
    ai_model: GPTModel
    open_api: OpenAPI
    base_url: str
    headers: dict[str, str]
