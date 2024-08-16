from typing import Optional, Sequence, TypeVar

T = TypeVar('T')


class Cursor[T]:
    def __init__(self, seq: Sequence[T]):
        self.current = 0
        self.total = len(seq)
        self.seq = seq

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

    def advance_if(self, expected_char: str) -> Optional[T]:
        if self.peek() == expected_char:
            return self.advance()
        return None

    def previous(self) -> Optional[T]:
        return self.seq[self.current - 1]

    def next(self) -> None:
        self.current += 1

    @property
    def has_any(self) -> bool:
        return self.current < self.total

    def __repr__(self):
        return f"Peek: {self.peek()}; Index: {self.current}; Total: {self.total}"
