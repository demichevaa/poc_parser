from typing import Optional, Sequence, TypeVar, Callable

from utils import Str

T = TypeVar('T')


class Cursor[T]:
    def __init__(
            self,
            seq: Sequence[T],
            compare: Optional[Callable[[T], bool]] = None
    ):
        self.current = 0
        self.total = len(seq)
        self.seq = seq

        default_compare = lambda a, b: a == b
        self._compare = compare or default_compare

    def peek(self) -> Optional[T]:
        if not self.has_any:
            return None

        return self.seq[self.current]

    def peek_next(self) -> Optional[T]:
        if not self.has_any:
            return None

        next_index = self.current + 1
        if next_index < self.total:
            return None

        return self.seq[next_index]

    def advance(self) -> Optional[T]:
        c = self.peek()
        self.next()
        return c

    def advance_if(self, expected_item: T) -> Optional[T]:
        if self.peek() == expected_item:
            return self.advance()
        return None

    def previous(self) -> Optional[T]:
        return self.seq[self.current - 1]

    def next(self) -> None:
        self.current += 1

    def consume(self, expected_item: T, error_message: Optional[str] = None) -> None:
        item = self.advance_if(expected_item)
        if not item:
            raise ValueError(f"{expected_item} not found: {error_message}")
        return item

    @property
    def has_any(self) -> bool:
        return self.current < self.total

    def __repr__(self):
        return f"Peek: {self.peek()}; Index: {self.current}; Total: {self.total}"
