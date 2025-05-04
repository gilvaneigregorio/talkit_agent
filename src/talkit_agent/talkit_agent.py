from uuid import UUID, uuid4

from agents import Agent, Runner, trace

from .agents import talkit_agent
from .chat import Chat, ChatMessage
from .context import AgentContext
from .models import ROLE_ASSISTANT, ROLE_USER, GPTModel
from .open_api import OpenAPI

WORKFLOW_NAME = "Conversation"


class TalkitAgent:
    def __init__(
        self,
        ai_model: GPTModel,
        open_api: OpenAPI,
        base_url: str,
        headers: dict[str, str],
    ) -> None:
        """
        Initialize the TalkitAgent with an AI model, OpenAPI specification,
        base URL, and headers.

        Args:
            ai_model (GPTModel): The AI model to be used for conversation.
            open_api (OpenAPI): The OpenAPI specification for the API.
            base_url (str): The base URL for the API.
            headers (dict[str, str]): Headers to be used in API requests.
        """
        self.chats = {}
        self.starting_agent: Agent = talkit_agent
        self.agent_context = AgentContext(ai_model, open_api, base_url, headers)

    def create_chat(self) -> UUID:
        """Create a new chat and return its ID."""

        chat_id = uuid4()
        self.chats[chat_id] = Chat()
        return chat_id

    def get_chat(self, chat_id: UUID) -> Chat | None:
        """Get a chat by ID. Returns None if not found."""
        return self.chats.get(chat_id)

    def list_chats(self) -> list[UUID]:
        """List all available chat IDs."""
        return list(self.chats.keys())

    def delete_chat(self, chat_id: UUID) -> bool:
        """Delete a chat by ID. Returns True if deleted, False if not found."""
        if chat_id in self.chats:
            del self.chats[chat_id]
            return True
        return False

    async def send_message(self, prompt: str, chat_id: UUID) -> ChatMessage:
        """Send a message to a specific chat. Creates a new chat if chat_id is None."""
        if chat_id not in self.chats:
            raise Exception(f"Chat with ID {chat_id} not found.")

        chat = self.chats[chat_id]
        with trace(workflow_name=WORKFLOW_NAME):
            chat.send_message(prompt, ROLE_USER)
            result = await Runner.run(
                starting_agent=self.starting_agent,
                input=chat.messages,
                context=self.agent_context,
            )

            chat_message = chat.send_message(result.final_output, ROLE_ASSISTANT)
            return chat_message
