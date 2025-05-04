import os

from openai import OpenAI
from pydantic import BaseModel

# Constants for role names
ROLE_DEVELOPER = "developer"
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"


DEFALT_MODEL = "gpt-4o-mini"


class GPTModel:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        """
        Initialize the GPTModel with an API key and model name.
        Args:
            api_key (str | None): The OpenAI API key. If None,
                it will be set from the environment variable.
            model (str | None): The model name to use. If None, sets to default.
        """

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        self.client = OpenAI()
        self.model_name = model or DEFALT_MODEL

    def call(
        self,
        input: list[dict[str, str]],
        tools: dict[str, str] | None = None,
        output_format: BaseModel | None = None,
    ) -> str:
        """
        Call the OpenAI API with the provided input and optional tools and output format.

        Args:
            input (list[dict[str, str]]): The input data for the API call.
            tools (dict[str, str] | None): Optional tools to use in the API call.
            output_format (BaseModel | None): Optional output format for the response.
        Returns:
            str: The output text from the API response.
        """
        kwargs = {
            "model": self.model_name,
            "input": input,
        }

        if tools:
            kwargs["tools"] = tools
        if output_format:
            kwargs["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": output_format.__class__.__name__,
                    "schema": output_format.model_json_schema(),
                    "strict": True,
                }
            }
        response = self.client.responses.create(**kwargs)

        return response.output_text
