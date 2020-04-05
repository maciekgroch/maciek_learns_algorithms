import unittest


class Node(object):
    """Representation of a stack node

    :param data: data to be stored in the node
    :type data: object
    :param next: pointer to the next node:
    :type next: Node

    """
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Stack(object):
    """My implementation of a stack.

    :param top: reference to the top node
    :type top: Node
    :param size: size of the stack
    :type size: int

    """
    def __init__(self):
        self.top = None
        self.size = 0

    def __repr__(self):
        current = self.top
        reprint = "["
        while current is not None:
            reprint += f"{current.data}, "
            current = current.next
        return reprint[:-2] + ']'

    def push(self, data):
        """Pushes to the stack

        :param data: data to be pushed
        :type data: object
        :Example:
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack
        [1]
        """
        node = Node(data)
        if self.top is None:  # initialization
            self.top = node
        else:
            node.next = self.top
            self.top = node
        self.size += 1

    def pop(self):
        """Pops the top (data is removed from the stack)

        :Example:
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.pop()
        1
        """
        if self.top is None:  # empty stack
            return None
        else:
            top = self.top.data
            self.top = self.top.next
            self.size -= 1
            return top

    def peak(self):
        """Peaks the top (data is NOT removed from the stack)

        :Example:
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.peak()
        1
        """
        if self.top is None:  # empty stack
            return None
        else:
            return self.top.data


class TestStack(unittest.TestCase):
    def test_init(self):
        stack = Stack()
        data_set = [(None, stack.top), (0, stack.size)]
        for expected, actual in data_set:
            with self.subTest(expected=expected, actual=actual):
                self.assertEqual(expected, actual)

    def test_push(self):
        stack = Stack()
        stack.push(1)
        expected, actual = 1, stack.top.data
        with self.subTest(expected=expected, actual=actual):
            self.assertEqual(expected, actual)
        stack.push(2)
        expected, actual = 2, stack.top.data
        with self.subTest(expected=expected, actual=actual):
            self.assertEqual(expected, actual)
        expected_size, actual_size = 2, stack.size
        with self.subTest(expected=expected_size, actual=actual_size):
            self.assertEqual(expected_size, actual_size)

    def test_pop_empty_stack(self):
        stack = Stack()
        expected = None
        actual = stack.pop()
        self.assertEqual(expected, actual)

    def test_pop_one_element(self):
        stack = Stack()
        stack.push(1)
        expected, actual = 1, stack.pop()
        self.assertEqual(expected, actual)

    def test_pop_push_pop(self):
        stack = Stack()
        stack.push(1)
        _ = stack.pop()
        stack.push(2)
        expected, actual = 2, stack.pop()
        with self.subTest(expected=expected, actual=actual):
            self.assertEqual(expected, actual)
        expected_size, actual_size = 0, stack.size
        with self.subTest(expected=expected_size, actual=actual_size):
            self.assertEqual(expected_size, actual_size)

    def test_push_100_elems_pop(self):
        stack = Stack()
        [stack.push(i) for i in range(100)]
        expected, actual = 99, stack.pop()
        with self.subTest(expected=expected, actual=actual):
            self.assertEqual(expected, actual)
        expected_size, actual_size = 99, stack.size
        with self.subTest(expected=expected_size, actual=actual_size):
            self.assertEqual(expected_size, actual_size)
        print(stack)

    def test_peak_empty_stack(self):
        stack = Stack()
        expected = None
        actual = stack.peak()
        self.assertEqual(expected, actual)

    def test_peak_one_element(self):
        stack = Stack()
        stack.push(1)
        expected, actual = 1, stack.peak()
        with self.subTest(expected=expected, actual=actual):
            self.assertEqual(expected, actual)
        expected_size, actual_size = 1, stack.size
        with self.subTest(expected=expected_size, actual=actual_size):
            self.assertEqual(expected_size, actual_size)

