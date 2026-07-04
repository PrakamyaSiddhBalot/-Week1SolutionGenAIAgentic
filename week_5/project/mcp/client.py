from mcp.loader import load_mcp_config


class MCPClient:

    def __init__(self):

        self.config = load_mcp_config()

        self.servers = {}

        self.tools = {}

    def connect(self):

        raise NotImplementedError

    def list_servers(self):

        return list(
            self.servers.keys()
        )

    def list_tools(self):

        return list(
            self.tools.keys()
        )
    def get_server_configs(self):
    
         return self.config.get(
            "mcpServers",
            {}
        )
