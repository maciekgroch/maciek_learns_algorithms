import unittest
from unittest import mock


class DisjointSet(object):
    def __init__(self, data):
        self._data = {v: v for v in data}
        self._ranks = {v: 0 for v in data}

    def find(self, v, path_compression=True):
        """Finds the root to which `v` is connected

        :param v: data for which the root is found
        :type v: hashable
        :param path_compression: should paths be compressed?
        :type path_compression: bool
        :raises KeyError: when v not in set
        :return: the root of disjoint set to which v is connected
        :rtype: hashable

        :Example:
        >>> disjoint_set = DisjointSet(['A', 'B', 'C'])
        >>> disjoint_set.find('A')  # A is connected to itself
        'A'
        """
        self._verify_if_in_set(v)
        if path_compression:
            root = self._find_with_path_compression(v)
        else:
            root = self._find(v)
        return root

    def _find_with_path_compression(self, v):
        if v != self._data[v]:
            self._data[v] = self._find_with_path_compression(self._data[v])
        return self._data[v]

    def _find(self, v):
        while v != self._data[v]:
            v = self._data[v]
        return v

    def union(self, u, v, path_compression=True):
        """Connects sets in which `u` and `v` are located

        :param u: first vertex (element of the set)
        :type u: hashable
        :param v: second vertex (element of the set)
        :type v: hashable
        :param path_compression: should the path be compressed?
        :type path_compression: bool
        :raises KeyError: when u or v not in the set

        :Example:
        >>> disjoint_set = DisjointSet(['A', 'B', 'C'])
        >>> disjoint_set.union('A', 'B')
        >>> disjoint_set.find('B')
        'A'
        """
        self._verify_if_in_set(u, v)
        root_u = self.find(u, path_compression)
        root_v = self.find(v, path_compression)
        if root_u == root_v:
            return
        rank_root_u = self._ranks[root_u]
        rank_root_v = self._ranks[root_v]
        if rank_root_u > rank_root_v:
            self._data[v] = root_u
        else:
            self._data[u] = root_v
            if rank_root_u == rank_root_v:
                self._ranks[root_v] += 1

    def _verify_if_in_set(self, *args):
        """Verify if elements provided in `*args` are in the set"""
        for u in args:
            if u not in self._data.keys():
                raise KeyError(f'{u} not in the set.')


class DisjointSetTestCase(unittest.TestCase):
    """Using example from Figure 5.6 in
        Dasgupta, Sanjoy, Christos H. Papadimitriou, and Umesh V. Vazirani.
        *Algorithms*. Boston: McGraw-Hill Higher Education, 2008
    """
    def test_init(self):
        expected_data = dict(A='A', B='B', C='C')
        expected_ranks = dict(A=0, B=0, C=0)
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        with self.subTest():
            self.assertDictEqual(expected_data, disjoint_set._data)
        with self.subTest():
            self.assertDictEqual(expected_ranks, disjoint_set._ranks)

    def test_verify_if_in_set_raises(self):
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        with self.assertRaises(KeyError):
            disjoint_set._verify_if_in_set('A', 'X')

    def test_verify_if_in_set_doesnt_raise(self):
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set._verify_if_in_set('A', 'B')  # no exception should be raised.
        self.assertEqual('passed', 'passed')

    def test_find_fully_disjoint(self):
        """A, B, C"""
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        for vertex, expected in [('A', 'A'), ('B', 'B'), ('C', 'C')]:
            with self.subTest('W/o path compression', vertex=vertex, expected=expected):
                obtained = disjoint_set._find(vertex)
                self.assertEqual(expected, obtained)
            with self.subTest('With path compression', vertex=vertex, expected=expected):
                obtained = disjoint_set._find_with_path_compression(vertex)
                self.assertEqual(expected, obtained)

    def test_find_a_to_b(self):
        """A--->B, C"""
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set._data['A'] = 'B'
        for vertex, expected in [('A', 'B'), ('B', 'B'), ('C', 'C')]:
            with self.subTest(vertex=vertex, root=expected):
                obtained = disjoint_set._find(vertex)
                self.assertEqual(expected, obtained)

    def test_find_a_to_b_with_path_compression(self):
        """A--->B, C"""
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set._data['A'] = 'B'
        for vertex, expected in [('A', 'B'), ('B', 'B'), ('C', 'C')]:
            with self.subTest(vertex=vertex, root=expected):
                obtained = disjoint_set._find_with_path_compression(vertex)
                self.assertEqual(expected, obtained)

    def test_find_a_to_b_path_compression(self):
        """A--->B, C"""
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set._data['A'] = 'B'
        expected = 'B'
        obtained = disjoint_set._find('A')
        self.assertEqual(expected, obtained)

    def test_find_a_to_b_to_c(self):
        """A--->B--->C"""
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set._data['A'] = 'B'
        disjoint_set._data['B'] = 'C'
        for vertex, expected in [('A', 'C'), ('B', 'C'), ('C', 'C')]:
            with self.subTest(vertex=vertex, expected=expected):
                obtained = disjoint_set._find(vertex)
                self.assertEqual(expected, obtained)

    def test_find_a_to_b_to_c_path_not_compressed(self):
        """A--->B--->C"""
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set._data['A'] = 'B'
        disjoint_set._data['B'] = 'C'
        for vertex, expected in [('A', 'B'), ('B', 'C'), ('C', 'C')]:
            with self.subTest(vertex=vertex, expected=expected):
                _ = disjoint_set._find(vertex)
                obtained = disjoint_set._data[vertex]
                self.assertEqual(expected, obtained)

    def test_find_a_to_b_to_c_with_path_compression(self):
        """A--->B--->C"""
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set._data['A'] = 'B'
        disjoint_set._data['B'] = 'C'
        for vertex, expected in [('A', 'C'), ('B', 'C'), ('C', 'C')]:
            with self.subTest(vertex=vertex, expected=expected):
                obtained = disjoint_set._find_with_path_compression(vertex)
                self.assertEqual(expected, obtained)

    def test_find_a_to_b_to_c_path_compressed(self):
        """A--->B--->C"""
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set._data['A'] = 'B'
        disjoint_set._data['B'] = 'C'
        for vertex, expected in [('A', 'C'), ('B', 'C'), ('C', 'C')]:
            with self.subTest(vertex=vertex, expected=expected):
                _ = disjoint_set._find_with_path_compression(vertex)
                obtained = disjoint_set._data[vertex]
                self.assertEqual(expected, obtained)

    @mock.patch.object(DisjointSet, '_find')
    def test_correct_find_is_used(self, mock_find):
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        _ = disjoint_set.find('A', path_compression=False)
        mock_find.assert_called_once_with('A')

    @mock.patch.object(DisjointSet, '_find_with_path_compression')
    def test_correct_find_is_used(self, mock_find):
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        _ = disjoint_set.find('A', path_compression=True)
        mock_find.assert_called_once_with('A')

    def test_union_a_b(self):
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set.union('A', 'B')
        test_set = [('A', 'B', 0), ('B', 'B', 1), ('C', 'C', 0)]
        self._test_union(disjoint_set, test_set)

    def test_union_same_root(self):
        disjoint_set = DisjointSet(['A', 'B', 'C'])
        disjoint_set.union('A', 'C')
        disjoint_set.union('B', 'C')
        test_set = [('A', 'C', 0), ('B', 'C', 0), ('C', 'C', 1)]
        self._test_union(disjoint_set, test_set)

    def test_union_rank_big_set(self):
        disjoint_set = DisjointSet(['A', 'B', 'C', 'D', 'E', 'F'])
        disjoint_set.union('A', 'C')
        disjoint_set.union('C', 'B')
        disjoint_set.union('E', 'A')
        disjoint_set.union('F', 'D')
        test_set = [('A', 'C', 0), ('B', 'C', 0), ('C', 'C', 1), ('D', 'D', 1), ('E', 'C', 0), ('F', 'D', 0)]
        self._test_union(disjoint_set, test_set)

    def _test_union(self, disjoint_set, test_set):
        for vertex, parent, rank in test_set:
            with self.subTest('Checking if parent was updated...', vertex=vertex, parent=parent):
                self.assertEqual(parent, disjoint_set._data[vertex])
            with self.subTest('Checking if rank was updated...', vertex=vertex, rank=rank):
                self.assertEqual(rank, disjoint_set._ranks[vertex])
