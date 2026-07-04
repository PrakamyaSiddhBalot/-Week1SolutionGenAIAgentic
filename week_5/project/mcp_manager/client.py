import os
from typing import Optional
from contextlib import AsyncExitStack

from dotenv import load_dotenv

from mcp import (
    ClientSession,
    StdioServerParameters
)

from mcp.client.stdio import (
    stdio_client
)

from mcp_manager.loader import load_mcp_config

load_dotenv()


class MCPClient:

    def __init__(self):

        self.config = load_mcp_config()

        self.session: Optional[ClientSession] = None

        self.exit_stack = AsyncExitStack()

        self.read = None

        self.write = None

        self.tools = {}

    def create_server_parameters(
        self,
        server_name
    ):

        servers = self.config.get(
            "mcpServers",
            {}
        )

        if server_name not in servers:

            raise ValueError(
                f"Unknown MCP server: {server_name}"
            )

        server = servers[server_name]

        env = {}

        for key, value in server["env"].items():

            if (
                value.startswith("${")
                and value.endswith("}")
            ):

                variable = value[2:-1]

                env[key] = os.environ.get(
                    variable,
                    ""
                )

            else:

                env[key] = value

        command = server["command"]

        # PowerShell uses npx.cmd
        if command == "npx":

            command = "npx.cmd"

        return StdioServerParameters(
            command=command,
            args=server["args"],
            env=env
        )

    async def connect(
        self,
        server_name
    ):

        params = self.create_server_parameters(
            server_name
        )

        stdio_transport = (
            await self.exit_stack.enter_async_context(
                stdio_client(params)
            )
        )

        self.read, self.write = stdio_transport

        self.session = (
            await self.exit_stack.enter_async_context(
                ClientSession(
                    self.read,
                    self.write
                )
            )
        )

        await self.session.initialize()
        response = await self.session.list_tools()

        self.tools = {}
        
        for tool in response.tools:
        
            self.tools[tool.name] = tool
        
        print(
            "Available tools:"
        )
        
        for tool_name in self.tools:
        
            print(
                "-",
                tool_name
            )
        
        print(
            f"Connected to {server_name} MCP server."
        )

    async def cleanup(self):

        await self.exit_stack.aclose()
