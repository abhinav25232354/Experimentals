"""Stack and Queue implementation samples."""

from collections import deque


class Stack:
    """Simple stack implementation using a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Push an item onto the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


class Queue:
    """Simple queue implementation using collections.deque."""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the item from the front of the queue."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def front(self):
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._items[0]

    def is_empty(self):
        """Return True if the queue is empty."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self._items)

    def __repr__(self):
        return f"Queue({list(self._items)})"


def main():
    stack = Stack()
    print("Stack sample")
    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("After pushes:", stack)
    print("Peek:", stack.peek())
    print("Pop:", stack.pop())
    print("After pop:", stack)
    print("Stack size:", stack.size())

    print("\nQueue sample")
    queue = Queue()
    queue.enqueue("a")
    queue.enqueue("b")
    queue.enqueue("c")
    print("After enqueues:", queue)
    print("Front:", queue.front())
    print("Dequeue:", queue.dequeue())
    print("After dequeue:", queue)
    print("Queue size:", queue.size())


if __name__ == "__main__":
    main()
