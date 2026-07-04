class MCPClient:

    def __init__(self):

        self.servers = {}

        self.tools = {}

    def connect(self, config):

        raise NotImplementedError

    def list_servers(self):

        return list(self.servers.keys())

    def list_tools(self):

        return list(self.tools.keys())
