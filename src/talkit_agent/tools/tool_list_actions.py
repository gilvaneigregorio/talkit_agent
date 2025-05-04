from agents import RunContextWrapper, function_tool

from ..context import AgentContext


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
