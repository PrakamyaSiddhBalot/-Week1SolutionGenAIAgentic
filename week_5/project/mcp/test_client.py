import asyncio
import json
import os

from mcp import (
    ClientSession,
    StdioServerParameters
)

from mcp.client.stdio import (
    stdio_client
)
with open(
    "config.json",
    "r",
    encoding="utf-8"
) as f:

    config = json.load(f)

github = config["mcpServers"]["github"]

env = {}

for key, value in github["env"].items():

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

server = StdioServerParameters(

    command="npx.cmd",

    args=github["args"],

    env=env

)

print(server)
