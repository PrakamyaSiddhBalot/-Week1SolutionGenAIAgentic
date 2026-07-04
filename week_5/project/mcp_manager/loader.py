import json


def load_mcp_config():

    try:

        with open(
            "config.json",
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except FileNotFoundError:

        return {
            "mcpServers": {}
        }
