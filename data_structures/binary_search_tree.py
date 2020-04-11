import unittest


class Node(object):
    def __init__(self, data):
        self.data = data
        self.left_child = None
        self.right_child = None


class BST(object):
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Inserts data to the tree

        :param data: data to be inserted
        :type data: must overload __lt__, __gt__

        :Example:
        >>> bst = BST()
        >>> bst.insert(1)
        >>> bst.insert(10000)
        >>> bst.root.data, bst.root.right_child.data
        (1, 10000)
        """
        node = Node(data)
        if self.root is None:  # insertion of the first element
            self.root = node
        else:  # there is already something in the tree
            current = self.root
            while True:
                if data <= current.data:  # left child
                    if current.left_child is None:
                        current.left_child = node
                        return
                    else:
                        current = current.left_child
                else:  # right child
                    if current.right_child is None:
                        current.right_child = node
                        return
                    else:
                        current = current.right_child

    def remove(self, data):
        """Removes node containing data from the tree.

        This is definitely the most difficult algo I had to develop in here...

        :param data: data to be removed
        :type data: must overload __lt__, __gt__
        :Example:
        >>> bst = BST()
        >>> bst.insert(1)
        >>> bst.insert(10000)
        >>> bst.remove(1)
        >>> bst.root.data, bst.root.right_child
        (10000, None)
        """
        node, parent = self._find_node_with_parent(data)

        if node is None and parent is None:
            return

        children_num = 0
        if node.left_child is not None:
            children_num += 1
        if node.right_child is not None:
            children_num += 1

        if children_num == 0:
            if parent is None:  # working with root, root has no children
                self.root = None
            else:
                if node is parent.left_child:
                    parent.left_child = None
                else:
                    parent.right_child = None
        elif children_num == 1:
            if node.left_child is not None:
                next_node = node.left_child
            else:
                next_node = node.right_child

            if parent is None:
                self.root = next_node
            else:
                if node is parent.left_child:
                    parent.left_child = next_node
                else:
                    parent.right_child = next_node
        else:
            #  1. Turn right from node and look for the leftmost node
            parent_of_the_leftmost_node = node
            leftmost_node = node.right_child
            while leftmost_node.left_child:
                parent_of_the_leftmost_node = leftmost_node
                leftmost_node = leftmost_node.left_child
            node.data = leftmost_node.data
            # In case the leftmost node has a right child
            if parent_of_the_leftmost_node.right_child == leftmost_node:
                # if we are here we never entered the while loop.
                parent_of_the_leftmost_node.right_child = leftmost_node.right_child
            else:  # we got inside the while loop
                parent_of_the_leftmost_node.left_child = leftmost_node.right_child

    def _find_node_with_parent(self, data):
        current = self.root
        previous = None
        while current:
            if data == current.data:
                return current, previous
            elif data <= current.data:
                previous = current
                current = current.left_child
            elif data >= current.data:
                previous = current
                current = current.right_child
        return None, None

    def find_min(self):
        """Find min value in the tree

        All you have to do is go left all the time

        :return: node with min data
        :rtype: Node
        :Example:
        >>> bst = BST()
        >>> bst.insert(1)
        >>> bst.insert(10000)
        >>> bst.insert(0)
        >>> bst.insert(-1)
        >>> bst.find_min().data
        -1
        """
        if self.root is None:
            return None
        current = self.root
        while current.left_child:
            current = current.left_child
        return current

    def find_max(self):
        """Find max value in the tree

        All you have to do is go right all the time

        :return: node with max value
        :rtype: Node
        :Example:
        >>> bst = BST()
        >>> bst.insert(1)
        >>> bst.insert(10000)
        >>> bst.insert(0)
        >>> bst.insert(1023021)
        >>> bst.find_max().data
        1023021
        """
        if self.root is None:
            return None
        current = self.root
        while current.right_child:
            current = current.right_child
        return current

    def find(self, data):
        """Finds the node with data, returns None if data not in the tree

        :param data: data to be removed
        :type data: must overload __lt__, __gt__
        :return: node with data
        :rtype: Node
        :Example:
        >>> bst = BST()
        >>> bst = BST()
        >>> bst.insert(5)
        >>> [bst.insert(i) for i in [3, 7, 8, 6, 2, 4, 1]]
        >>> node = bst.find(7)
        >>> node.left_child.data, node.right_child.data
        (6, 8)
        """
        if self.root is None:
            return None
        current = self.root
        while current:
            if data == current.data:
                return current
            elif data <= current.data:
                current = current.left_child
            elif data > current.data:
                current = current.right_child
        return None


class TestBST(unittest.TestCase):
    """Test cases taken from:
    Basant Agarwal and Benjamin Baka
        Hands-On Data Structures and Algorithms with Python: Write complex and
        powerful code using the latest features of Python 3.7,
    Packt 2018
    """
    def test_init(self):
        bst = BST()
        self.assertIsNone(bst.root)

    def test_insert_first_element(self):
        bst = BST()
        bst.insert(1)
        data_set = [
            (1, bst.root.data),
            (None, bst.root.left_child),
            (None, bst.root.right_child)
        ]
        for expected, actual in data_set:
            with self.subTest(expected=expected, actual=actual):
                self.assertEqual(expected, actual)

    def test_insert(self):
        """Considering case:
                        5
                3               7
            2       4      6         8
        1
        """
        bst = BST()
        bst.insert(5)  # we need to make sure 5 is in the root to have right balance
        [bst.insert(i) for i in [3, 7, 8, 6, 2, 4, 1]]
        data_set = [
            (bst.root.data, 5),
            (bst.root.left_child.data, 3),
            (bst.root.left_child.left_child.data, 2),
            (bst.root.left_child.right_child.data, 4),
            (bst.root.left_child.left_child.left_child.data, 1),

            (bst.root.right_child.data, 7),
            (bst.root.right_child.left_child.data, 6),
            (bst.root.right_child.right_child.data, 8)
        ]
        for actual, expected in data_set:
            with self.subTest(expected=expected, actual=actual):
                self.assertEqual(expected, actual)

    def test_find_min(self):
        """Considering case:
                        5
                3               7
            2       4      6         8
        1

        So the minimum is 1
        """
        bst = BST()
        bst.insert(
            5)  # we need to make sure 5 is in the root to have right balance
        [bst.insert(i) for i in [3, 7, 8, 6, 2, 4, 1]]
        bst_min = bst.find_min()
        self.assertEqual(1, bst_min.data)

    def test_find_min_only_root(self):
        bst = BST()
        bst.insert(5)
        bst_min = bst.find_min()
        self.assertEqual(5, bst_min.data)

    def test_find_min_empty_tree(self):
        bst = BST()
        bst_min = bst.find_min()
        self.assertIsNone(bst_min)

    def test_find_max(self):
        """Considering case:
                        5
                3               7
            2       4      6         8
        1

        So the maximum is 8
        """
        bst = BST()
        bst.insert(
            5)  # we need to make sure 5 is in the root to have right balance
        [bst.insert(i) for i in [3, 7, 8, 6, 2, 4, 1]]
        bst_max = bst.find_max()
        self.assertEqual(8, bst_max.data)

    def test_find_max_only_root(self):
        bst = BST()
        bst.insert(5)
        bst_max = bst.find_max()
        self.assertEqual(5, bst_max.data)

    def test_find_max_empty_tree(self):
        bst = BST()
        bst_max = bst.find_max()
        self.assertIsNone(bst_max)

    def test_find_node_with_parent_empty_tree(self):
        bst = BST()
        node, parent = bst._find_node_with_parent(5)
        for actual in [node, parent]:
            with self.subTest(actual=actual):
                self.assertIsNone(actual)

    def test_find_node_with_parent_root(self):
        bst = BST()
        bst.insert(5)
        node, parent = bst._find_node_with_parent(5)
        for expected, actual in [(5, node.data), (parent, None)]:
            with self.subTest(expected=expected, actual=actual):
                self.assertEqual(expected, actual)

    def test_find_node_with_paren_complex_tree(self):
        """Considering case:
                        5
                3               7
            2       4      6         8
        1

        """
        bst = BST()
        bst.insert(
            5)  # we need to make sure 5 is in the root to have right balance
        [bst.insert(i) for i in [3, 7, 8, 6, 2, 4, 1]]
        data_set = [  # data, expected_node.data, expected_parent.data,
            (1, 1, 2), (2, 2, 3), (4, 4, 3), (6, 6, 7), (112, None, None)
        ]
        for i, expected_node_data, expected_parent_data in data_set:
            node, parent = bst._find_node_with_parent(i)
            actual_node_data = node.data if node is not None else None
            actual_parent_data = parent.data if parent is not None else None
            with self.subTest(
                        expected_node_data=expected_node_data,
                        acutal_node_data=actual_node_data,
                        expected_parent_data=expected_parent_data,
                        actual_parent_data=actual_parent_data):
                self.assertEqual(expected_node_data, actual_node_data)
                self.assertEqual(expected_parent_data, actual_parent_data)

    def test_remove_root_no_children(self):
        # 1. Remove root, just root
        bst = BST()
        bst.insert(1)
        bst.remove(1)
        test_set1 = [(None, bst.root)]
        self._test_set(test_set1)

    def test_remove_left_leaf(self):
        """2. Remove left leaf (3)
        Considering case:
                        5               remove(3) ->         5
                3               7                      (None)      7
        """
        bst = BST()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        bst.remove(3)
        test_set1 = [
            (5, bst.root.data),
            (None, bst.root.left_child),
            (7, bst.root.right_child.data)
        ]
        self._test_set(test_set1)

    def test_remove_right_leaf(self):
        """3. Remove right leaf (7)
        Considering case:
                        5               remove(7) ->         5
                3               7                      3           (None)
        """
        bst = BST()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        bst.remove(7)
        test_set1 = [
            (5, bst.root.data),
            (None, bst.root.right_child),
            (3, bst.root.left_child.data)
        ]
        self._test_set(test_set1)

    def test_remove_root_with_1_children_left(self):
        """4. Remove left child (3)
        Considering case:
                        5           ------------>            3
                3                                     None            None
        """
        bst = BST()
        bst.insert(5)
        bst.insert(3)
        bst.remove(5)
        test_set1 = [
            (3, bst.root.data),
            (None, bst.root.left_child),
            (None, bst.root.right_child)
        ]
        self._test_set(test_set1)

    def test_remove_root_with_1_children_right(self):
        """5. Remove right child (7)
        Considering case:
                        5           ------------>            7
                            7                       None            None
        """
        bst = BST()
        bst.insert(5)
        bst.insert(7)
        bst.remove(5)
        test_set1 = [
            (7, bst.root.data),
            (None, bst.root.left_child),
            (None, bst.root.right_child)
        ]
        self._test_set(test_set1)

    def test_remove_node_with_one_child_left(self):
        """6. Remove node 3
        Considering case:
                        5           ------------>            5
                3               7                      1            7
        1
        """
        bst = BST()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        bst.insert(1)
        bst.remove(3)
        test_set1 = [
            (5, bst.root.data),
            (1, bst.root.left_child.data),
            (7, bst.root.right_child.data)
        ]
        self._test_set(test_set1)

    def test_remove_node_with_one_child_left(self):
        """7. Remove node 4
        Considering case:
                        5           ------------>            5
                3               7                      4           7
                    4
        """
        bst = BST()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        bst.insert(4)
        bst.remove(3)
        test_set1 = [
            (5, bst.root.data),
            (4, bst.root.left_child.data),
            (7, bst.root.right_child.data)
        ]
        self._test_set(test_set1)

    def test_remove_root_with_2_children(self):
        """8. Remove root (5)
        Considering case:
                        5           ------------>            7
                3               7                      3            None
        """
        bst = BST()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        bst.remove(5)
        test_set1 = [
            (7, bst.root.data),
            (3, bst.root.left_child.data),
            (None, bst.root.right_child)
        ]
        self._test_set(test_set1)

    def test_remove_root_with_2_children_complex(self):
        """9. Remove root (5
        Considering case:
                        5           ------------>            6
                3               7                      3            7
                            6       8                                   8
        """
        bst = BST()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        bst.insert(8)
        bst.insert(6)
        bst.remove(5)
        test_set1 = [
            (6, bst.root.data),
            (3, bst.root.left_child.data),
            (7, bst.root.right_child.data),
            (8, bst.root.right_child.right_child.data)
        ]
        self._test_set(test_set1)

    def test_remove_node_with_2_children_complex(self):
        """10. Remove node 10
        Considering case:
                        3
                   2           10
             1          6              14
        0                       11              15
                                    12

        We should get:
                        3
                   2           11
             1          6            14
        0                      12            15

        """
        bst = BST()
        bst.insert(3)
        bst.insert(2)
        bst.insert(10)
        bst.insert(1)
        bst.insert(6)
        bst.insert(14)
        bst.insert(0)
        bst.insert(11)
        bst.insert(15)
        bst.insert(12)

        bst.remove(10)
        test_set1 = [
            (3, bst.root.data),
            (2, bst.root.left_child.data),
            (1, bst.root.left_child.left_child.data),
            (0, bst.root.left_child.left_child.left_child.data),

            (11, bst.root.right_child.data),
            (6, bst.root.right_child.left_child.data),
            (14, bst.root.right_child.right_child.data),
            (15, bst.root.right_child.right_child.right_child.data),
            (12, bst.root.right_child.right_child.left_child.data),
        ]
        self._test_set(test_set1)

    def _test_set(self, test_set):
        for expected, actual in test_set:
            with self.subTest(expected=expected, actual=actual):
                self.assertEqual(expected, actual)

    def test_find_empty_tree(self):
        bst = BST()
        node = bst.find(10)
        self.assertIsNone(node)

    def test_find_not_in_the_tree(self):
        """Considering case:
                        5
                3               7
            2       4      6         8
        1
        """
        bst = BST()
        bst.insert(
            5)  # we need to make sure 5 is in the root to have right balance
        [bst.insert(i) for i in [3, 7, 8, 6, 2, 4, 1]]
        node = bst.find(100050012031)
        self.assertIsNone(node)

    def test_find_in_the_tree(self):
        """Considering case:
                        5
                3               7
            2       4      6         8
        1
        """
        bst = BST()
        bst.insert(
            5)  # we need to make sure 5 is in the root to have right balance
        [bst.insert(i) for i in [3, 7, 8, 6, 2, 4, 1]]
        node = bst.find(7)
        test_set = [(6, node.left_child.data), (8, node.right_child.data)]
        self._test_set(test_set)


