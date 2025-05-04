class ChatMessage:
    def __init__(self, role: str, content: str) -> None:
        """
        Initialize a chat message with a role and content.
        Args:
            role (str): The role of the message sender (e.g., "user", "assistant").
            content (str): The content of the message.
        """
        self.role = role
        self.content = content

    def to_dict(self) -> dict:
        """
        Convert the chat message to a dictionary format.
        Returns:
            dict: A dictionary representation of the chat message.
        """
        return {"role": self.role, "content": self.content}


class Chat:
    def __init__(self) -> None:
        """
        Initialize a chat session with an empty list of messages.
        """
        self.messages: list = []

    def send_message(self, message: str, role: str) -> ChatMessage:
        """
        Send a message in the chat session.
        Args:
            message (str): The content of the message.
            role (str): The role of the message sender (e.g., "user", "assistant").
        Returns:
            ChatMessage: The created chat message object.
        """
        chat_message = ChatMessage(role, message)
        self.messages.append(chat_message.to_dict())
        return chat_message

    def list_messages(self) -> list[ChatMessage]:
        """
        List all messages in the chat session.
        Returns:
            list[ChatMessage]: A list of chat messages.
        """
        return self.messages
