from typing import Optional

from node import ObjList


class LinkedList:
    """
    Model of double linked list.

    - **head** - pointer to the first node in the linked list.
    - **tail** - pointer to the last node in the linked list.
    """

    __length: int

    def __init__(
        self,
        head: Optional[ObjList] = None,
        tail: Optional[ObjList] = None
    ) -> None:
        self.head = head
        self.tail = tail

        if not self.head or not self.tail:
            self.__length = 0

        else:
            self.__length = self.__count_nodes()

    def __count_nodes(self) -> int:
        """Counts nodes in a non-empty linked list."""
        count: int = 0
        node: ObjList = self.head

        while node:
            count += 1
            node = node.get_next()

        return count

    def __len__(self):
        return self.__length

    def is_empty(self) -> bool:
        """Return True if LinkedList is empty."""
        return not self.head or not self.tail or self.__length == 0

    def add_obj(self, obj: Optional[ObjList]) -> None:
        """Add a new ObjList to the end of a linked list."""
        if not obj:
            return

        if self.is_empty():
            self.head = self.tail = obj
            self.__length += 1
            return

        self.tail.set_next(obj)
        prev_node: ObjList = self.tail
        self.tail = obj
        self.tail.set_prev(prev_node)

        self.__length += 1

    def remove_obj(self) -> None:
        """Remove a ObjList from the end of a linked list."""
        if self.is_empty():
            raise IndexError('pop from an empty LinkedList')

        prev_node: ObjList = self.tail.get_prev()
        data: str = self.tail.get_data()
        self.tail.set_prev(None)
        self.tail = prev_node

        if self.tail:
            self.tail.set_next(None)

        self.__length -= 1
        return data

    def get_data(self) -> list[str]:
        """Get a list of data from all ObjList in a linked list."""
        if self.is_empty():
            return []

        data_list: list[str] = []
        node: Optional[ObjList] = self.head

        while node:
            data_list.append(node.get_data())
            node = node.get_next()

        return data_list
