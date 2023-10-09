from metaclasses import Singletone
from servers import Data, Server


class Router(metaclass=Singletone):
    """Router model."""

    buffer: list[Data]
    __linked_servers: dict[str, Server]

    def __init__(self) -> None:
        self.buffer = []
        self.__linked_servers = {}

    def is_linked(self, ip: int) -> bool:
        """Checking the connection between the router and the server via IP."""
        return ip in self.__linked_servers

    def link(self, server: Server) -> None:
        """Connectiong the server to the router."""
        self.__linked_servers[server.ip] = server

    def unlink(self, server: Server) -> None:
        """Disconnecting the server from the router."""
        if self.is_linked(server.ip):
            del self.__linked_servers[server.ip]

    def send_data(self) -> None:
        """
        Sending data packets from the router buffer
        to specified server. After sending data
        the router buffer is cleared.
        """
        for data in self.buffer:
            if self.is_linked(data.ip):
                server = self.__linked_servers.get(data.ip)
                server.buffer.append(data.data)

        self.buffer.clear()
