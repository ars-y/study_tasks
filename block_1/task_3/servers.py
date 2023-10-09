from copy import deepcopy
from typing import Optional

import routers
from storages import ipdb


class Data:
    """Data packet model."""

    def __init__(self, data: str, ip: int) -> None:
        self.data = data
        self.ip = ip


class Server:
    """Server model."""

    buffer: list[Data]
    __servers_created_number: int = 0

    def __init__(self, ip: Optional[int] = None) -> None:
        type(self).__servers_created_number += 1

        self.ip = self._get_or_create_ip(ip)
        self.buffer = []

    def __del__(self) -> None:
        if type(self).__servers_created_number > 0:

            server_number: int = type(self).__servers_created_number
            if server_number in ipdb:
                ipdb.remove(server_number)

            type(self).__servers_created_number -= 1

    def _get_or_create_ip(self, ip: Optional[int]) -> int:
        """Returns an unoccupied IP-address."""
        if not ip:
            n: int = type(self).__servers_created_number
            for server_number in range(1, n + 1):
                if server_number not in ipdb:
                    ipdb.add(server_number)
                    return server_number

        if ip not in ipdb:
            ipdb.add(ip)

        return ip

    def send_data(self, data: Data) -> None:
        """Send data to router."""
        router = routers.Router()
        if router.is_linked(self.ip):
            router.buffer.append(data)

    def get_data(self) -> list[Data]:
        """Returns a list of recieved data packets and clear buffer."""
        data: list[Data] = deepcopy(self.buffer)
        self.buffer.clear()
        return data

    def get_ip(self) -> int:
        """Return server IP-address."""
        return self.ip
