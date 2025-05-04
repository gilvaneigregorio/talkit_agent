import json

import requests
from agents import RunContextWrapper, function_tool

from ..context import AgentContext


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
