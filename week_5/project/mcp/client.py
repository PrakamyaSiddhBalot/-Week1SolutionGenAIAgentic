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

from mcp.loader import load_mcp_config


load_dotenv()


class MCPClient:

    def __init__(self):

        self.config = load_mcp_config()

        self.session: Optional[
            ClientSession
        ] = None

        self.exit_stack = (
            AsyncExitStack()
        )

        self.tools = {}
    def create_server_parameters(
        self,
        server_name
    ):

        servers = (
            self.config.get(
                "mcpServers",
                {}
            )
        )

        if server_name not in servers:

            raise ValueError(
                f"Unknown MCP server: {server_name}"
            )

        server = servers[
            server_name
        ]

        env = {}

        for key, value in server[
            "env"
        ].items():

            if (
                value.startswith("${")
                and value.endswith("}")
            ):

                variable = value[2:-1]

                env[key] = (
                    os.environ.get(
                        variable,
                        ""
                    )
                )

            else:

                env[key] = value

        command = server[
            "command"
        ]

        if command == "npx":

            command = "npx.cmd"

        return (
            StdioServerParameters(
                command=command,
                args=server["args"],
                env=env
            )
        )
