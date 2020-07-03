import unittest


def find_max_wis(path_graph):
    """Calculates maximum weight independent set of the given path graph.
    I follow the dynamic programming solution with a memoization table.

    :param path_graph: input path graph
    :type path_graph: list
    :return: vertices building the wis, total weight
    :rtype: tuple(list, int)

    **Example**
    >>> path_graph = [5, 7, 8, 2, 9, 12]
    >>> wis, weight = find_max_wis(path_graph)
    >>> wis, weight
    {5, 8 12}, 25
    """
    wis_table = _build_wis_table(path_graph)
    reconstructed_set = _reconstruct(wis_table, path_graph)
    return reconstructed_set, wis_table[-1]


def _build_wis_table(path_graph):
    """Walks through the input path_graph and builds memoization table.
    :param path_graph: input path_graph
    :type path_graph: list
    :return:  memoization table
    :rtype: list
    """
    wis_table = [0 for _ in range(len(path_graph) + 1)]
    wis_table[1] = path_graph[0]
    for i in range(2, len(wis_table)):
        wis_table[i] = max(
            wis_table[i - 1],
            wis_table[i - 2] + path_graph[i - 1]
        )
    return wis_table


def _reconstruct(wis_table, path_graph):
    """Reconstructs the the maximum weight independent set from the memoization
    table. Returns

    :param wis_table: memoization table
    :type wis_table: list
    :param path_graph: graph used for reconstruction
    :type path_graph: list
    :return: maximum weight independent set
    :rtype: set
    """
    i = len(wis_table) - 1
    reconstructed = set()
    while i >= 1:
        if wis_table[i] == wis_table[i-1]:
            i -= 1
        else:
            reconstructed.add(path_graph[i-1])
            i -= 2
    return reconstructed


class TestWis(unittest.TestCase):
    def test_build_wis_table(self):
        path_graph = [5, 7, 8, 2, 9, 12]
        memoization_table = _build_wis_table(path_graph)
        expected = [0, 5, 7, 13, 13, 22, 25]
        self.assertListEqual(expected, memoization_table)

    def test_reconstruct(self):
        path_graph = [5, 7, 8, 2, 9, 12]
        wis_table = [0, 5, 7, 13, 13, 22, 25]
        expected = {5, 8, 12}
        actual = _reconstruct(wis_table, path_graph)
        self.assertSetEqual(expected, actual)

    def test_find_max_wis(self):
        path_graph = [5, 7, 8, 2, 9, 12]
        wis, weight = find_max_wis(path_graph)
        with self.subTest(expected_wis={5, 8, 12}, actual_wis=wis):
            self.assertSetEqual({5, 8, 12}, wis)
        with self.subTest(expected_weight=25, actual_weight=weight):
            self.assertEqual(25, weight)
