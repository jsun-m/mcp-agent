import inspect
from typing import Callable, Any, Optional

from autogen import ConversableAgent


def from_ag2_agent(
    agent: ConversableAgent,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Callable[..., Any]:
    """
    Convert an AG2 ConversableAgent to a plain Python function.

    The resulting function takes a message string, sends it to the agent,
    and returns the agent's reply as a string.

    Args:
        agent: The AG2 ConversableAgent to convert.
        name: Optional override for the function name.
        description: Optional override for the function docstring.

    Returns:
        Callable[..., Any]: Function with correct signature and metadata.
    """
    # Set name with fallback
    if name:
        func_name = name
    elif hasattr(agent, "name") and agent.name:
        func_name = agent.name.replace(" ", "_").lower()
    else:
        func_name = "ag2_agent_func"

    # Set description with fallback
    if description:
        func_doc = description
    elif hasattr(agent, "description") and agent.description:
        func_doc = agent.description
    elif hasattr(agent, "system_message") and agent.system_message:
        func_doc = agent.system_message
    else:
        func_doc = f"Send a message to the {func_name} agent and get a reply."

    def wrapper(message: str) -> str:
        """Send a message to the AG2 agent and return its reply."""
        reply = agent.generate_reply(
            messages=[{"content": message, "role": "user"}],
        )

        # Handle different reply types
        if isinstance(reply, dict):
            return reply.get("content", "")
        elif isinstance(reply, str):
            return reply
        else:
            return ""

    # Set metadata
    wrapper.__name__ = func_name
    wrapper.__doc__ = func_doc
    wrapper.__signature__ = inspect.Signature(
        [inspect.Parameter("message", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str)]
    )
    wrapper.__annotations__ = {"message": str, "return": str}

    return wrapper
