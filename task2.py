"""Вопрос №2

На языке Python написать минимум по 2 класса реализовывающих циклический буфер FIFO. Объяснить плюсы и минусы каждой 
реализации.

Оценивается:

Полнота и качество реализации
Оформление кода
Наличие сравнения и пояснения по быстродействию
"""

# Реализация 1
from abc import ABC, abstractmethod
from typing import Any, Iterable, Iterator


class CircularBuffer(ABC):

    def __init__(self, iterable: Iterable = None, size: int = 256):
        self._validate_parameters(iterable, size)

    @staticmethod
    def _validate_parameters(iterable: Iterable, size: int) -> None:
        if iterable is not None and not isinstance(iterable, Iterable):
            raise TypeError("iterable must be an instance of Iterable")
        if not isinstance(size, int):
            raise TypeError("size must be an integer")
        if size < 1:
            raise ValueError("size must be greater than zero")

    @abstractmethod
    def append(self, item: Any) -> None:
        pass

    @abstractmethod
    def popleft(self) -> None:
        pass

    @abstractmethod
    def is_empty(self) -> None:
        pass


class CircularBufferList(CircularBuffer):

    def __init__(self, iterable: Iterable = None, size: int = 256):
        super().__init__(iterable, size)
        if iterable is None:
            iterable = []

        self._buffer = [None] * size
        self._size = size
        self._head = 0
        self._tail = 0
        self._is_full = False

        for item in iterable:
            self.append(item)

    def append(self, item: Any) -> None:
        self._buffer[self._tail] = item
        if self._is_full:
            self._head = (self._head + 1) % self._size
        self._tail = (self._tail + 1) % self._size
        self._is_full = self._tail == self._head

    def popleft(self) -> Any:
        if self.is_empty():
            raise IndexError(f"Buffer is empty.")
        item = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % self._size
        self._is_full = False
        return item

    def is_empty(self) -> bool:
        return self._buffer[self._head] is None and self._buffer[self._tail] is None

    def __iter__(self) -> Iterator:
        if self.is_empty():
            buffer = []
        elif self._head < self._tail:
            buffer = self._buffer[self._head : self._tail]
        else:
            buffer = self._buffer[self._head :] + self._buffer[: self._tail]
        yield from buffer

    def __repr__(self) -> str:
        cir_buffer = list(self)
        return f"{self.__class__.__name__}({cir_buffer}, size={self._size})"


# Реализация 2
class Node:

    def __init__(self, value: Any):
        self.value = value
        self.next: Node | None = None


class CircularBufferNode(CircularBuffer):

    def __init__(self, iterable: Iterable = None, size: int = 256):
        super().__init__(iterable, size)
        if iterable is None:
            iterable = []

        self._size = size
        self._head = None
        self._tail = None
        self._count = 0

        for item in iterable:
            self.append(item)

    def append(self, value: int) -> None:
        new_node = Node(value)
        if self._count == 0:
            self._head = new_node
            self._tail = new_node
            new_node.next = new_node
        elif self._count < self._size:
            new_node.next = self._head
            self._tail.next = new_node
            self._tail = new_node
        else:
            new_node.next = self._head.next
            self._tail.next = new_node
            self._tail = new_node
            self._head = new_node.next

        if self._count < self._size:
            self._count += 1

    def popleft(self) -> Any:
        if self.is_empty():
            raise IndexError("Buffer is empty")

        value = self._head.value
        if self._count == 1:
            self._head = None
            self._tail = None
        else:
            self._tail.next = self._head.next
            self._head = self._head.next
        self._count -= 1
        return value

    def is_empty(self) -> bool:
        return self._count == 0

    def __iter__(self) -> Iterator:
        current = self._head
        for _ in range(self._count):
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        cir_buffer = list(self)
        return f"{self.__class__.__name__}({cir_buffer}, size={self._size})"


"""Вывод:

Представлено две реализации в первой CircularBufferList данные сохраняются в списке (list), а во второй 
CircularBufferNode в связанном списке реализованном с помощью Node. Операции вставки и удаления (append и popleft) в 
обеих реализациях выполняются за O(1). Первый способ работает быстрее, так как в начале создается фиксированный список,
после чего элементы добавляются и удаляются по индексам в списке за O(1), во втором же случае постоянно создаются новые
объекты Node на, что уходит дополнительное время. Но второй способ эффективнее по памяти, так как в нем сразу не 
создается список, а Node добавляются по мере необходимости, кроме того второй способ на основе связанного списка может 
быть более гибким в том случае, если необходимо было бы динамически изменять размер очереди. В tests корректность работы
проверяется в сравнении с встроенной в python структурой данных deque.
"""
