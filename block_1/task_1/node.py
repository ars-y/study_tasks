from typing import Optional


class ObjList:
    """Model of a ObjList.

    Args:
    - **data** - str with data stored in the ObjList;
    - **next** - pointer to next ObjList;
    - **prev** - pointer to previous ObjList.
    """

    def __init__(
        self,
        data: Optional[str] = None,
        next: Optional['ObjList'] = None,
        prev: Optional['ObjList'] = None
    ) -> None:
        self.__data = data
        self.__next = next
        self.__prev = prev

    def set_next(self, obj: Optional['ObjList']) -> None:
        """Set a ponter of the next ObjList to obj from argument."""
        self.__next = obj

    def set_prev(self, obj: Optional['ObjList']) -> None:
        """Set a ponter of the previous ObjList to obj from argument."""
        self.__prev = obj

    def get_next(self) -> Optional['ObjList']:
        """Get value from next ObjList pointer."""
        return self.__next

    def get_prev(self) -> Optional['ObjList']:
        """Get value from previous ObjList pointer."""
        return self.__prev

    def set_data(self, data: str) -> None:
        """Set data to ObjList."""
        self.__data = data

    def get_data(self) -> str:
        """Get data from ObjList."""
        return self.__data
