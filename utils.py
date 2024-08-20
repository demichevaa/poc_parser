from enum import Enum, EnumMeta
from typing import Protocol


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.value


class Str(Protocol):
    def __str__(self) -> str:
        pass
