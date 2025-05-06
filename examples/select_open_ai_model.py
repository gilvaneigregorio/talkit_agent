import asyncio
import os

from talkit_agent import TalkitAgent
from talkit_agent.ai_models import AIModelClient
from talkit_agent.open_api import OpenAPIClient

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
                    },
                    "400": {"description": "Bad request"},
                },
            }
        }
    },
}


async def main():
    talkit_agent = TalkitAgent(
        base_url="https://api.example.com",
        headers={"Authorization": "Bearer YOUR_API_KEY"},
        open_api_client=OpenAPIClient(spec),
        ai_model_client=AIModelClient(
            api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o"
        ),
    )

    chat_id = talkit_agent.create_chat()

    chat_message = await talkit_agent.send_message(
        chat_id=chat_id, prompt="List all users"
    )
    print(f"Chat ID: {chat_id} - Message: {chat_message.content}")


if __name__ == "__main__":
    asyncio.run(main())
