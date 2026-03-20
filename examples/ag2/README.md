# AG2 ConversableAgent Integration Example

This example demonstrates integrating an AG2 (formerly AutoGen) ConversableAgent into
MCP Agent as a tool. The AG2 agent acts as a specialist — when the MCP Agent needs to
solve a math problem, it delegates to the AG2 ConversableAgent and uses its reply.

## App Setup

Clone the repo and navigate to the AG2 example:

```bash
git clone https://github.com/lastmile-ai/mcp-agent.git
cd mcp-agent/examples/ag2
```

Install `uv` (if you don't have it):

```bash
pip install uv
```

Sync `mcp-agent` project dependencies:

```bash
uv sync --extra ag2
```

Install requirements specific to this example:

```bash
uv pip install -r requirements.txt
```

## Set up API Keys

Create a `.env` file in this directory with your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Run the Example

Run your MCP Agent app:

```bash
uv run main.py
```
