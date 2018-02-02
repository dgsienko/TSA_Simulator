# Author: Brian O'Neill
# Combined module for array-based and linked queues for the Goodrich et. al
# data structures textbook. Created for CS/IT 200 class.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class ArrayQueue:
    """FIFO Queue implementation using a Python list as underlying storage"""
    DEFAULT_CAPACITY = 100  # moderate capacity for all new queues

    def __init__(self):
        """Constructor"""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        """Return the number of elements in this queue"""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty"""
        return self._size == 0

    def first(self):
        """Return (but do not remove) the element at the front of the queue.

        Raise IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError('Queue is empty')
        return self._data[self._front]

    def dequeue(self):
        """Remove and return the first element of the queue.

        Raise IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        """Add an element to the back of the queue."""
        if self._size == len(self._data):
            self._resize(2*len(self._data))  # Double the array size
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):
        """Resize to a new list of capacity cap >= len(self)."""
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0


class LinkedQueue:
    """FIFO Queue implementation using a singly linked list for storage"""
    # ----------------------- nested _Node class -------------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = '_element', '_next'     # Streamline memory usage

        def __init__(self, e, n):
            self._element = e         # Reference to item contained
            self._next = n               # Reference to next node

    # ------------------------ stack methods -----------------------------------
    def __init__(self):
        """Constructor"""
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but do not remove) the element at the front of the queue"""
        if self.is_empty():
            raise IndexError('Queue is empty')
        return self._head._element

    def dequeue(self):
        """Remove and return the first element of the queue.

        Raise IndexError if queue is empty.
        """
        if self.is_empty():
            raise IndexError('Queue is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():     # Special case as queue is empty
            self._tail = None   # Removed head had also been the tail
        return answer

    def enqueue(self, e):
        """Add element e to the back of the queue."""
        newest = self._Node(e, None)    # Node will be new tail node
        if self.is_empty():
            self._head = newest         # Special case: Previously empty
        else:
            self._tail._next = newest
        self._tail = newest             # Update reference to tail node
        self._size += 1
