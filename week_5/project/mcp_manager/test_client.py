import asyncio

from mcp_manager.client import MCPClient


async def main():

    client = MCPClient()

    try:

        print("Connecting to GitHub MCP server...")

        await client.connect("github")

        print("Connection successful!")

    finally:

        await client.cleanup()


if __name__ == "__main__":

    asyncio.run(main())
