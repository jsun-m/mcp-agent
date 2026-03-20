import asyncio
import os
import time

from dotenv import load_dotenv

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.tools.ag2_tool import from_ag2_agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from autogen import ConversableAgent, LLMConfig

# Load env variables
load_dotenv()

app = MCPApp(name="ag2_example")


async def example_usage():
    async with app.run() as agent_app:
        logger = agent_app.logger

        # Create an AG2 ConversableAgent as a specialist
        llm_config = LLMConfig(
            api_type="openai",
            model="gpt-4o-mini",
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        with llm_config:
            math_agent = ConversableAgent(
                name="math_expert",
                system_message="You are a math expert. Solve math problems step by step and return the final answer.",
                human_input_mode="NEVER",
                description="A math expert agent that can solve mathematical problems.",
            )

        # Wrap the AG2 agent as a tool for mcp-agent
        agent = Agent(
            name="assistant",
            instruction="You are a helpful assistant. Use the math_expert tool to solve any math problems.",
            server_names=[],
            functions=[from_ag2_agent(math_agent)],
        )

        async with agent:
            llm = await agent.attach_llm(OpenAIAugmentedLLM)

            result = await llm.generate_str(
                message="What is the sum of the first 10 prime numbers?",
            )

            logger.info(f"Result: {result}")


if __name__ == "__main__":
    start = time.time()
    asyncio.run(example_usage())
    end = time.time()
    t = end - start

    print(f"Total run time: {t:.2f}s")
