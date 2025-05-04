from agents import Agent

from .context import AgentContext
from .tools.tool_execute_action import execute_action
from .tools.tool_get_action import get_action
from .tools.tool_list_actions import list_actions

talkit_agent = Agent[AgentContext](
    name="Talkit Agent",
    instructions="""
        Your task is to assist the user in executing actions he wants to perform.

        Given a prompt, you should, do the following:
        1. List all the actions that can be performed.
        2. Retrieve the action that best matches the prompt.
        3. Execute the action and return the result.
        4. If the action is not found, ask at once the user for all the details 
            needed to execute the action. If possible provide an example of the 
            action.
        5. If you don't have enough information to execute the action, resoning on 
            that and may try to find an action that can help get the missing 
            information.
        6. If even after reasoning you don't find an action that can help, ask the 
            user for more details.
    """,
    tools=[list_actions, get_action, execute_action],
)
