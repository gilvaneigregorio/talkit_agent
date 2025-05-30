# talkit_agent

Talkit Agent turns any OpenAPI spec into a conversational API assistant. It understands user prompts, picks the right endpoint, makes the call, and returns the result. Just talk to your API.

## Installation

You can install the talkit_agent package using pip:

```bash
pip install talkit-agent
```

Or clone the repository and install locally:

```bash
git clone https://github.com/your-username/talkit_agent.git
cd talkit_agent
pip install -e .
```

## Requirements

- Python 3.12 or later
- OpenAI API key

## Usage

```python
import asyncio
import os
from talkit_agent import TalkitAgent
from talkit_agent.ai_models import AIModelClient
from talkit_agent.open_api import OpenAPIClient

# Define your OpenAPI spec
spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "Example API",
        "version": "1.0.0",
    },
    "paths": {
        "/api/users": {
            "get": {
                "summary": "Get all users",
                "description": "Returns a list of all users in the system",
                "operationId": "getUsers",
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "name": {"type": "string"},
                                            "email": {"type": "string"},
                                        },
                                    },
                                }
                            }
                        },
                    }
                },
            }
        }
    },
}

async def main():
    # Initialize the TalkitAgent
    talkit_agent = TalkitAgent(
        base_url="https://api.example.com",
        headers={"Authorization": "Bearer YOUR_API_KEY"},
        open_api_client=OpenAPIClient(spec),
        ai_model_client=AIModelClient(api_key=os.getenv("OPENAI_API_KEY")),
    )

    # Create a new chat
    chat_id = talkit_agent.create_chat()

    # Send a message to the chat
    chat_message = await talkit_agent.send_message(
        chat_id=chat_id, prompt="List all users"
    )
    print(f"Chat ID: {chat_id} - Message: {chat_message.content}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### TalkitAgent

The main class that manages conversations and interactions with APIs.

- `__init__(base_url, headers, open_api_client, ai_model_client)`: Initialize the agent
- `create_chat()`: Create a new chat session and return its ID
- `get_chat(chat_id)`: Get a chat by ID
- `list_chats()`: List all available chat IDs
- `delete_chat(chat_id)`: Delete a chat by ID
- `send_message(chat_id, prompt)`: Send a message to a chat and get AI response

### OpenAPIClient

Handles OpenAPI specification parsing and operation management.

- `__init__(spec)`: Initialize with an OpenAPI spec dictionary
- `from_string(data)`: Create from a JSON string
- `from_file(path)`: Create from a JSON file
- `list_operations()`: List all available API operations
- `get_operation_details(path, method)`: Get details of an operation
- `get_operation_details_by_id(operation_id)`: Get operation details by ID

### AIModelClient

Manages interactions with OpenAI models.

- `__init__(api_key=None, model=None)`: Initialize with an API key and model name
- `call(input, tools=None, output_format=None)`: Call the OpenAI API

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
