import json

import requests
from agents import RunContextWrapper, function_tool
from pydantic import BaseModel, ConfigDict

from .ai_models import ROLE_DEVELOPER, ROLE_USER
from .context import AgentContext


@function_tool
def list_actions(wrapper: RunContextWrapper[AgentContext]) -> str:
    """
    Retrieve a list of actions that can be performed.

    Args:
        wrapper (RunContextWrapper[AgentContext]): The context wrapper containing the
            agent context.

        Returns:
            str: A list of dictionaries containing operation_id and description.
    """
    open_api_spec = wrapper.context.open_api
    actions = []
    operations = open_api_spec.list_operations()
    for operation in operations:
        operation_details = open_api_spec.get_operation_details(
            operation["path"], operation["method"]
        )
        actions.append(
            {
                "operation_id": operation_details.get("operationId", ""),
                "description": operation_details.get("description", ""),
            }
        )

    return str(actions)


class OperationId(BaseModel):
    operation_id: str

    model_config = ConfigDict(extra="forbid")


@function_tool
def get_action(
    wrapper: RunContextWrapper[AgentContext],
    prompt: str,
    actions: str,
) -> str:
    """
    Get the most relevant action based on the prompt and available actions.

    Args:
        wrapper (RunContextWrapper[AgentContext]): The context wrapper containing the
            agent context.
        prompt (str): The prompt to be used for the action.
        actions (str): A string representation of the actions to be performed.

    Returns:
        str: The action details that best match the prompt.
    """
    input = [
        {
            "role": ROLE_DEVELOPER,
            "content": "You are an software engineer expert in OpenAPI specifications.",
        },
        {
            "role": ROLE_USER,
            "content": f"""
                Given the following operations with their summary, descriptions and id,
                retrieve the operationId from the most relevant operation based on the
                prompt.

                **Prompt:**
                {prompt}

                **Actions:**
                {actions}
            """,
        },
    ]

    ai_model = wrapper.context.ai_model
    action = ai_model.call(input=input, output_format=OperationId)
    action = json.loads(action)["operation_id"]
    open_api_spec = wrapper.context.open_api
    action_detail = open_api_spec.get_operation_details_by_id(action)
    return action_detail


@function_tool
def execute_action(
    wrapper: RunContextWrapper[AgentContext],
    method: str,
    url: str,
    body: str,
) -> str:
    """
    Execute an action.

    Args:
        method (str): The HTTP method (GET, POST, PUT, DELETE, etc.)
        url (str): The URL to send the request to
        headers (str): The headers to send with the request it should be a JSON string
        body (str): The body to send with the request

    Returns:
        str: The response from the request
    """
    body = json.loads(body) if body != "" else {}
    headers = wrapper.context.headers
    url = f"{wrapper.context.base_url}{url}"

    respose = requests.request(method=method, url=url, headers=headers, json=body)
    response_json = respose.json()
    success = False
    if respose.status_code >= 200 and respose.status_code < 300:
        success = True

    return {
        "success": success,
        "status_code": respose.status_code,
        "response": response_json,
    }
