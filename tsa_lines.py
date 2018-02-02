"""
Dillon Sienko
CS 200
10/5/2017
Lab 6
tsa_lines.py
"""

import queues

class ScannerLane(queues.ArrayQueue):
    """Implementation/extension of Array Queue class to model a scanner line in a TSA Airport simulation."""
    
    def __init__(self):
        """Constructor"""
        self._data = [None] * queues.ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0
        
class IDLine(queues.LinkedQueue):
    """Implementation/extension of Linked Queue class to model an ID line in a TSA Airport simulation."""
    
    # ----------------------- nested _Node class -------------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node representing a single passenger."""
        __slots__ = '_element', '_next'     # Streamline memory usage

        def __init__(self, e, n):
            self._element = e            # Reference to item contained
            self._next = n               # Reference to next node

    # ------------------------ queue methods -----------------------------------
    
    def __init__(self):
        """Constructor"""
        self._head = None
        self._tail = None
        self._size = 0
        
    
        
    
    
    