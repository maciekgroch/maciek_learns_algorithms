import unittest


class Node(object):
    """
   Representation of a singly linked list nodes

    :param data: data to be stored in the node
    :type data: object
    :param next: pointer to the next node:
    :type next: Node

    """
    def __init__(self, data=None):
        self.data = data
        self.next = None


class SinglyLinkedList(object):
    """
    Representation of a singly linked list:
        head -> node_2 -> node_3 -> ... -> node_i -> tail
    (head is first -- on the left, tail is last -- on the right)

    :param head: pointer to the head node of the list
    :type head: Node
    :param tail: pointer to the tail node of the list
    :type tail: Node
    :param size: number of nodes in the list
    :type size: int

    """
    def __init__(self):
        self.tail = None
        self.head = None
        self.__current = self.head
        self.size = 0

    def __contains__(self, data):
        current = self.tail
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def __iter__(self):
        self.__current = self.head
        return self

    def __next__(self):
        if self.__current is None:
            self.__current = self.head
            raise StopIteration
        else:
            current = self.__current
            self.__current = self.__current.next
            return current.data

    def __len__(self):
        return self.size

    def __repr__(self):
        current = self.head
        reprint = "["
        while current is not None:
            reprint += f"{current.data}, "
            current = current.next
        return reprint.strip() + ']'

    def append(self, data):
        """Appends (to tail -- to the right) data to the list.

        :param data: data to be appended
        :type data: object

        :Example:
        >>> my_list = SinglyLinkedList()
        >>> my_list.append(1)
        >>> my_list.append(2)
        >>> my_list
        [1, 2,]
        """
        node = Node(data)
        self.size += 1
        if self.tail is not None:
            self.tail.next = node
            self.tail = node
        else:  # First node in the list
            self.head = node
            self.tail = node

    def appendleft(self, data):
        """Appends (to head -- to the left) data to the list.

        :param data: data to be appended
        :type data: object

        :Example:
        >>> my_list = SinglyLinkedList()
        >>> my_list.appendleft(1)
        >>> my_list.appendleft(2)
        >>> my_list
        [2, 1,]
        """
        node = Node(data)
        self.size += 1
        if self.head is not None:
            node.next = self.head
            self.head = node
        else:  # First node in the list
            self.head = node
            self.tail = node

    def delete(self, data):
        """Appends (to head -- to the left) data to the list.

        :param data: data to be removed
        :type data: object

        :Example:
        >>> my_list = SinglyLinkedList()
        >>> my_list.appendleft(1)
        >>> my_list.appendleft(2)
        >>> my_list.delete(1)
        >>> my_list
        [2,]
        """
        current = self.head
        previous = self.head
        while current:
            if current.data == data:
                if current == self.head:
                    self.head = current.next
                else:
                    previous.next = current.next
                    if current == self.tail:
                        self.tail = previous
                self.size -= 1

            previous = current
            current = current.next


class TestNodeCase(unittest.TestCase):
    def test_node_init(self):
        data = 'foo'
        node = Node(data)
        # To asserts in one test method. I do know I should split it 2.
        self.assertEqual(data, node.data)
        self.assertEqual(None, node.next)


class TestSinglyLinkedList(unittest.TestCase):
    def test_init(self):
        expected = [None, None, 0]
        my_list = SinglyLinkedList()
        actual = my_list.head, my_list.tail, my_list.size
        for e, a in zip(expected, actual):
            with self.subTest(e=e, a=a):
                self.assertEqual(e, a)

    def test_append_first_element(self):
        my_list = SinglyLinkedList()
        my_list.append('foo')
        expected = ['foo', 'foo', 1, None, None]
        actual = [
            my_list.head.data, my_list.tail.data, my_list.size,
            my_list.tail.next, my_list.head.next
        ]
        self._test_append(expected, actual)

    def test_append(self):
        my_list = SinglyLinkedList()
        my_list.append('foo')
        my_list.append('bar')
        my_list.append('baz')
        expected = ['foo', 'baz', 3]
        actual = [my_list.head.data, my_list.tail.data, my_list.size]
        self._test_append(expected, actual)

    def test_appendleft_first_element(self):
        my_list = SinglyLinkedList()
        my_list.appendleft('foo')
        expected = ['foo', 'foo', 1]
        actual = [my_list.head.data, my_list.tail.data, my_list.size]
        self._test_append(expected, actual)

    def test_appendleft(self):
        my_list = SinglyLinkedList()
        my_list.appendleft('foo')
        my_list.appendleft('bar')
        my_list.appendleft('baz')
        expected = ['baz', 'foo', 3]
        actual = [my_list.head.data, my_list.tail.data, my_list.size]
        self._test_append(expected, actual)

    def _test_append(self, expected, actual):
        for e, a in zip(expected, actual):
            with self.subTest(e=e, a=a):
                self.assertEqual(e, a)

    def test_contains(self):
        my_list = SinglyLinkedList()
        my_list.appendleft('foo')
        my_list.appendleft('bar')
        data_set = ['foo', 'xyz']
        expected = [True, False]
        for data, e in zip(data_set, expected):
            with self.subTest(data=data, e=e):
                self.assertEqual(e, data in my_list)

    def test_iter(self):
        my_list = SinglyLinkedList()
        expected = list(range(100))
        [my_list.append(i) for i in expected]
        for e, a in zip(expected, my_list):
            with self.subTest(e=e, a=a):
                self.assertEqual(e, a)

    def test_delete_head(self):
        self._test_delete(0, 1, 99, 99)

    def test_delete_tail(self):
        self._test_delete(99, 0, 98, 99)

    def test_delete_middle(self):
        self._test_delete(55, 0, 99, 99)

    def _test_delete(self, elem_to_delete, head, tail, size):
        my_list = SinglyLinkedList()
        [my_list.append(i) for i in range(100)]
        my_list.delete(elem_to_delete)
        data_set = (
            (head, my_list.head.data),
            (tail, my_list.tail.data),
            (size, my_list.size)
        )
        for expected, actual in data_set:
            with self.subTest(expected=expected, actual=actual):
                self.assertEqual(expected, actual)

    def test_len(self):
        my_list = SinglyLinkedList()
        for i in range(1, 101):
            my_list.append(i)
            actual = len(my_list)
            with self.subTest(expected=i, actual=actual):
                self.assertEqual(i, actual)
