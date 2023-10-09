from typing import Any


class Singletone(type):

    __self = None

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if not cls.__self:
            cls.__self = super().__call__(*args, **kwds)
        return cls.__self
