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

    :Example:
    Let's consider a very simple graph: A -> B -> C
                                             |--> D
    >>> adjacency_dict = {'A': ['B'], 'B': ['C', 'D'], 'C': [], 'D': []}
    >>> visited, pre, post, clock = dfs(adjacency_dict, 'A')
    >>> visited
    defaultdict(<class 'bool'>, {'A': True, 'B': True, 'C': True, 'D': True})
    >>> pre
    {'A': 1, 'B': 2, 'C': 3, 'D': 5}
    >>> post
    {'C': 4, 'D': 6, 'B': 7, 'A': 8}

    Based on `pre` and `post` topological order of the graph can be build:

                            A (1, 8)
                            |
                            B (2, 7)
                            |
                        ----|----
                        |       |
                    C (3, 4)     D (5, 6)
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

    :Example:
    BFS can be used to find shortest paths from starting vertex to all other
    (connected) paths of the graph.
    >>> a_dict = {'A': ['B', 'E'], 'B': ['C'], 'C': ['D'], 'D': ['E'], 'E': []}
    A -> B -> C -> D -> E
     |---------------->
    >>> paths, distances = bfs(a_dict, 'A')
    >>> paths
    {'A': [], 'B': ['B'], 'E': ['E'], 'C': ['B', 'C'], 'D': ['B', 'C', 'D']})
    >>> distances
    >>> {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 1}
    """
    visited = defaultdict(bool)
    visited[start] = True
    queue = deque([start])

    paths = defaultdict(list)
    distances = dict()
    for v in adjacency_dict.keys():
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


def post_to_sorted_list(post):
    """
    Sorts a dict based on the values and returns keys
    :param post: dict with post values
    :type post: dict
    :return: list with vertices
    :rtype: list

    :Example:
    >>> post = {'A': 7, 'B': 3, 'C': 1, 'D': 17, 'E': 101, 'F': 5}
    >>> post_to_sorted_list(post)
    ['C', 'B', 'F', 'A', 'D', 'E']
    """
    return [k for k, _ in sorted(post.items(), key=lambda item: item[1])]


def find_sccs(adjacency_dict):
    """An algorithm to find strongly connected components (SCCs) of a directed
    acyclic graphs. My implementation of Kosaraju's algorithm.

    :param adjacency_dict: a directed acyclic graph represented as an adjacency
        dict
    :type adjacency_dict: dict
    :return: a list of all sccs, each find_sccs is a list of vertices
    :rtype: list

    :Example:
    >>> a_dict = {'A': ['B'], 'B': ['C'], 'C': ['A', 'D'], 'D': []}
    >>> find_sccs(a_dict)
    [['B', 'C', 'A'], ['D']]
    """
    visited = {v: False for v in adjacency_dict}
    pre = dict()
    post = dict()
    clock = 1

    for v in adjacency_dict:
        if not visited[v]:
            visited, pre, post, clock = dfs(
                adjacency_dict, v, visited, clock, pre, post
            )
    stack = post_to_sorted_list(post)

    reversed_adjacency_dict = defaultdict(list)
    for v, u_list in adjacency_dict.items():
        # Initialization -> creates empty list if v not in the dict,
        # does nothing otherwise
        _ = reversed_adjacency_dict[v]
        for u in u_list:
            reversed_adjacency_dict[u].append(v)
    reversed_visited = {u: False for u in reversed_adjacency_dict}
    sccs = list()

    while stack:
        pre = dict()
        post = dict()
        clock = 1
        v = stack.pop()
        if not reversed_visited[v]:
            visited, pre, post, clock = dfs(
                reversed_adjacency_dict, v, reversed_visited, clock, pre, post
            )
        scc = post_to_sorted_list(post)
        if scc:
            sccs.append(scc)

    return sccs


class TestSearching(unittest.TestCase):
    """For tests I am using graph from Fig. 3.7 in
    Dasgupta, Sanjoy, Christos H. Papadimitriou, and Umesh V. Vazirani.
    *Algorithms*. Boston: McGraw-Hill Higher Education, 2008
    """
    DFS_TEST_DICT = {
        'A': ['B', 'C', 'F'],
        'B': ['E'],
        'C': ['D'],
        'D': ['A', 'H'],
        'E': ['F', 'G', 'H'],
        'F': ['B', 'G'],
        'G': [],
        'H': ['G']
    }
    BFS_TEST_DICT = {  # And for this test (the same book) Fig 4.2
        'A': ['B', 'S'],
        'B': ['A', 'C'],
        'C': ['B', 'S'],
        'D': ['E', 'S'],
        'E': ['D', 'S'],
        'S': ['A', 'C', 'D', 'E']
    }
    POST_TO_SORTED_LIST_TEST_DICT = {
        'A': 7, 'B': 3, 'C': 1, 'D': 17, 'E': 101, 'F': 5
    }
    SCC_TEST_DICT = {  # Fig. 3.9
        'A': ['B'],
        'B': ['C', 'D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['B', 'F', 'G'],
        'F': ['C', 'H'],
        'G': ['H', 'J'],
        'H': ['K'],
        'I': ['G'],
        'J': ['I'],
        'K': ['L'],
        'L': ['J'],
    }

    def test_bfs(self):
        expected_paths = defaultdict(list)
        expected_paths.update({
            'A': ['A'],
            'B': ['A', 'B'],
            'C': ['C'],
            'D': ['D'],
            'E': ['E'],
            'S': []
        })
        expected_distances = {'A': 1, 'B': 2, 'C': 1, 'D': 1, 'E': 1, 'S': 0}
        expected = [expected_paths, expected_distances]
        actual = bfs(self.BFS_TEST_DICT, 'S')
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
        actual = dfs(self.DFS_TEST_DICT, 'A')
        for e, a in zip(expected, actual):
            with self.subTest(expected=e, actual=e):
                self.assertDictEqual(e, a)

    def test_post_to_sorted_list(self):
        expected = ['C', 'B', 'F', 'A', 'D', 'E']
        actual = post_to_sorted_list(self.POST_TO_SORTED_LIST_TEST_DICT)
        self.assertListEqual(expected, actual)

    def test_scc(self):
        expected_sccs = [
            ['A'],
            ['B', 'E'],
            ['C', 'F'],
            ['D'],
            ['G', 'H', 'I', 'J', 'K', 'L']
        ]
        actual_sccs = find_sccs(self.SCC_TEST_DICT)
        # find_sccs doesn't sort the answer...
        actual_sccs = [sorted(scc) for scc in actual_sccs]
        actual_sccs = sorted(actual_sccs, key=lambda scc: scc[0])
        for expected_scc, actual_scc in zip(expected_sccs, actual_sccs):
            with self.subTest(e=expected_sccs, a=actual_sccs):
                self.assertListEqual(expected_scc, actual_scc)
