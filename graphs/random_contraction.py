import copy
import unittest
from unittest.mock import patch

import numpy as np


def random_min_cut(adjacency_dict):
    """
    Randomly finds a minimum cut of a connected graph; implementation of
    Karger's algorithm: https://en.wikipedia.org/wiki/Karger%27s_algorithm

    :param adjacency_dict: a representation of an adjacency list
    :type adjacency_dict: dict(int: list)
    :return: size of the min cut
    :rtype: int

    :Example:
    Let's consider the following graph:
    1 --- 2 --- 3 --- 4
    No matter how we contract the graph (1 --- 234 / 12 --- 34 / 123 --- 4)
    We will end up with the minimum cut value of 1 (there's only one cut)

    :Example:
    >>> a_dict = {1: [2], 2: [1, 3], 3: [2]}
    >>> min_cut = random_min_cut(a_dict)
    >>> print(min_cut)
    1
    """
    a_dict = copy.deepcopy(adjacency_dict)
    while len(a_dict) > 2:
        v1 = np.random.choice(list(a_dict.keys()))
        v2 = np.random.choice(a_dict[v1])
        contract(a_dict, v1, v2)
    return len(a_dict[list(a_dict.keys())[0]])


def contract(a_dict, v1, v2):
    """
    Contracts edges between two vertices `v1` and `v2`. In this implementation
    contraction means that all edges from v2 will be moved to v1 and v2 will
    be removed:
    1. Let's consider the following graph: 1 --- 2 --- 3.
       In our representation: {1: [2], 2: [1, 3], 3: [2]}
    2. Edge 1 --- 2 is contracted: 1 --- 3
       In our representation: {1: [3], 3: [1]}

    TBH I didn't like the fact that a dict is manipulated inside the function;
    I would prefer copying the input dict and returning a new one. However, the
    latter is much less efficient than the former...

    :param a_dict:
    :param v1: index of the first vertex
    :type v1: int
    :param v2: index of the second vertex
    :type v1: int

    :Example:
    >>> a_dict = {1: [2], 2: [1, 3], 3: [2]}
    >>> contract(a_dict, v1, v2)
    >>> print(a_dict)
    {1: [3], 3: [1]}
    """
    a_dict[v2] = [v for v in a_dict[v2] if v != v1]
    a_dict[v1] = [v for v in a_dict[v1] if v != v2]
    a_dict[v1] += a_dict[v2]
    for vertex in a_dict[v2]:
        a_dict[vertex].append(v1)
        a_dict[vertex].remove(v2)
    del a_dict[v2]


class TestRandomMinCut(unittest.TestCase):
    A_DICT_1 = {1: [2], 2: [1, 3], 3: [2]}
    A_DICT_2 = {
        1: [2, 3, 4],
        2: [1, 5, 6, 4],
        3: [1, 5],
        4: [2, 1, 5],
        5: [2, 3, 4, 6],
        6: [2, 5]
    }

    @patch('numpy.random.choice')
    def test_random_min_cut(self, mock):
        """ Testing a random function is a bit tricky. While testing we cannot
        depend on luck, therefore, we need to eliminate the randomness of the
        algorithm using `mock.patch`; a list of vertices to be contracted is
        provided.
            [1, 2, 1, 3, 1, 4, 1, 5] -> consecutive pairs are subtracted
            (1, 2) -> (1, 3) -> (1, 4) -> (1, 5) leaving us with the min cut
            1_2_3_4_5 === 6 where the minimum cut is equal 2.
        """
        test_set = [
            (self.A_DICT_1, [1, 2], 1),
            (self.A_DICT_2, [1, 2, 1, 3, 1, 4, 1, 5], 2),
        ]
        for in_dict, vertices, expected in test_set:
            with self.subTest(
                    in_dict=in_dict, vertices=vertices, expected=expected
            ):
                mock.side_effect = vertices
                min_cut = random_min_cut(in_dict)
                self.assertEqual(min_cut, expected)

    def test_contract(self):
        test_set = [
            (self.A_DICT_1, 1, 2, {1: [3], 3: [1]}),
            (self.A_DICT_1, 2, 3, {1: [2], 2: [1]}),
            (self.A_DICT_2, 2, 6, {
                1: [2, 3, 4],
                2: [1, 5, 4, 5],  # Two edges 2 --- 5
                3: [1, 5],
                4: [2, 1, 5],
                5: [2, 3, 4, 2]  # Two edges 5 --- 2
            }),
        ]
        for in_dict, v1, v2, expected in test_set:
            with self.subTest(in_dict=in_dict, v1=v1, v2=v2, expected=expected):
                in_dict_copied = copy.deepcopy(in_dict)
                contract(in_dict_copied, v1, v2)
                self.assertDictEqual(in_dict_copied, expected)


if __name__ == '__main__':
    unittest.main()
