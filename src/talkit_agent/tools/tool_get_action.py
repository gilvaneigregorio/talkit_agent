import json

from agents import RunContextWrapper, function_tool
from pydantic import BaseModel, ConfigDict

from ..models import ROLE_DEVELOPER, ROLE_USER
from ..context import AgentContext


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
