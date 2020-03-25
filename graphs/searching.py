from collections import defaultdict, deque
import unittest

import numpy as np


def dfs(adjacency_dict, start, visited=None, clock=1, pre=None, post=None):
    """ (Recursive) Implementation of Depth First Search (DFS)

    :param adjacency_dict: a representation of an adjacency list
    :type adjacency_dict: dict(hashable: list)
    :param start: the vertex from which search is started
    :type start: hashable (the same type that was used as adjacency_dict keys
    :param visited: already visited vertices (for recursive calls)
    :type visited: dict
    :param clock: call counter
    :type clock: int
    :param pre: saves order pre procedure
    :type pre: dict
    :param post: saves order of post procedure
    :type post: dict
    :return: visited, pre-indices, post-indices, clock
    :rtype: tuple(dict, dict, dict, int)
    """
    if visited is None:
        visited = defaultdict(bool)
    visited[start] = True
    if pre is None:
        pre = dict()
    if post is None:
        post = dict()
    pre[start] = clock
    clock += 1

    for u in adjacency_dict[start]:
        if not visited[u]:
            visited, pre, post, clock = dfs(
                adjacency_dict, u, visited, clock, pre, post)
    post[start] = clock
    clock += 1
    return visited, pre, post, clock


def bfs(adjacency_dict, start):
    """ Implementation of Breadth First Search (BFS).

    :param adjacency_dict: a representation of an adjacency list
    :type adjacency_dict: dict(hashable: list)
    :param start: the vertex from which search is started
    :type start: hashable (the same type that was used as adjacency_dict keys
    :return: paths to all vertices, distances to all vertices
    :rtype: tuple(dict, dict)
    """
    visited = defaultdict(bool)
    visited[start] = True

    queue = deque([start])

    paths = defaultdict(list)
    distances = dict()
    for v in adjacency_dict.keys():
        paths[v].append(start)
        distances[v] = np.nan
    distances[start] = 0

    while queue:
        u = queue.pop()
        for v in adjacency_dict[u]:
            if visited[v]:
                continue
            queue.appendleft(v)
            visited[v] = True
            distances[v] = distances[u] + 1
            paths[v] = paths[u] + [v]
    return paths, distances


class TestSearching(unittest.TestCase):
    """For tests I am using graph from Fig. 3.7 in
    Dasgupta, Sanjoy, Christos H. Papadimitriou, and Umesh V. Vazirani.
    *Algorithms*. Boston: McGraw-Hill Higher Education, 2008
    """
    A_DICT_1 = {
        'A': ['B', 'C', 'F'],
        'B': ['E'],
        'C': ['D'],
        'D': ['A', 'H'],
        'E': ['F', 'G', 'H'],
        'F': ['B', 'G'],
        'G': [],
        'H': ['G']
    }
    """ And for this test (the same book) Fig 4.2 
    """
    A_DICT_2 = {
        'A': ['B', 'S'],
        'B': ['A', 'C'],
        'C': ['B', 'S'],
        'D': ['E', 'S'],
        'E': ['D', 'S'],
        'S': ['A', 'C', 'D', 'E']
    }

    def test_bfs(self):
        expected_paths = defaultdict(list)
        expected_paths.update({
            'A': ['S', 'A'],
            'B': ['S', 'A', 'B'],
            'C': ['S', 'C'],
            'D': ['S', 'D'],
            'E': ['S', 'E'],
            'S': ['S']
        })
        expected_distances = {'A': 1, 'B': 2, 'C': 1, 'D': 1, 'E': 1, 'S': 0}
        expected = [expected_paths, expected_distances]
        actual = bfs(self.A_DICT_2, 'S')
        for e, a in zip(expected, actual):
            with self.subTest(e=e, a=a):
                self.assertDictEqual(e, a)

    def test_dfs(self):
        expected_pre = {
            'A': 1, 'B': 2, 'C': 12, 'D': 13, 'E': 3, 'F': 4, 'G': 5, 'H': 8
        }
        expected_post = {
            'A': 16, 'B': 11, 'C': 15, 'D': 14, 'E': 10, 'F': 7, 'G': 6, 'H': 9
        }
        expected_visited = defaultdict(bool)
        for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            expected_visited[i] = True
        expected = [expected_visited, expected_pre, expected_post]
        actual = dfs(self.A_DICT_1, 'A')
        for e, a in zip(expected, actual):
            with self.subTest(expected=e, actual=e):
                self.assertDictEqual(e, a)

