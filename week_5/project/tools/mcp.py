import asyncio

from mcp_manager.client import MCPClient


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "mcp_call",
            "description":
                "Call any tool exposed by an MCP server.",
            "parameters": {
                "type": "object",
                "properties": {
                    "server": {
                        "type": "string",
                        "description":
                            "The MCP server name from config.json."
                    },
                    "tool": {
                        "type": "string",
                        "description":
                            "The MCP tool to execute."
                    },
                    "arguments": {
                        "type": "object",
                        "description":
                            "Arguments passed to the MCP tool."
                    }
                },
                "required": [
                    "server",
                    "tool",
                    "arguments"
                ]
            }
        }
    }
]


async def _mcp_call_async(
    server,
    tool,
    arguments
):

    client = MCPClient()

    try:

        await client.connect(server)

        result = await client.call_tool(
            tool,
            arguments
        )

        return result

    finally:

        await client.cleanup()


def mcp_call(
    server,
    tool,
    arguments
):

    return asyncio.run(
        _mcp_call_async(
            server,
            tool,
            arguments
        )
    )
