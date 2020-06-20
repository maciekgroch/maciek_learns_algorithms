from collections import defaultdict
import heapq
import unittest


def mst_prim(graph, start):
    """Finds the minimum spanning tree of `graph` using Prim's algorithm.

    :param graph: a directed graph adjacency dict: {v: (weight, u)}
    :type graph: dict
    :param start: start vertex
    :type start: object
    :return mst, total cost
    :rtype tuple(dict, float)
    """
    mst = defaultdict(list)
    heap = [(0, start, None)]
    visited = set()
    total_cost = 0
    while heap:
        cost, u, v = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        total_cost += cost
        if v is not None:
            mst[u].append((cost, v))
            mst[v].append((cost, u))
        for neighbour in graph[u]:
            if neighbour[1] in visited:
                continue
            heapq.heappush(heap, (*neighbour, u))
    return mst, total_cost


class TestMst(unittest.TestCase):
    """For tests I am using graph from Fig. 5.9 in
    Dasgupta, Sanjoy, Christos H. Papadimitriou, and Umesh V. Vazirani.
    *Algorithms*. Boston: McGraw-Hill Higher Education, 2008
    """
    PRIM_GRAPH_IN = {
        'A': [(5, 'B'), (6, 'C'), (4, 'D')],
        'B': [(5, 'A'), (1, 'C'), (2, 'D')],
        'C': [(6, 'A'), (1, 'B'), (2, 'D'), (5, 'E'), (3, 'F')],
        'D': [(4, 'A'), (2, 'B'), (2, 'C'), (4, 'F')],
        'E': [(5, 'C'), (4, 'F')],
        'F': [(3, 'C'), (4, 'D'), (4, 'E')]
    }
    PRIM_MST_EXPECTED = {
        'A': [(4, 'D')],
        'B': [(1, 'C'), (2, 'D')],
        'C': [(1, 'B'), (3, 'F')],
        'D': [(4, 'A'), (2, 'B')],
        'E': [(4, 'F')],
        'F': [(3, 'C'), (4, 'E')]
    }

    def test_mst_prim(self):
        expected_cost = 14
        mst, actual_cost = mst_prim(self.PRIM_GRAPH_IN, 'A')
        with self.subTest(
                expected_cost=expected_cost, actual_cost=actual_cost):
            self.assertEqual(expected_cost, actual_cost)
        for key in ['A', 'B', 'C', 'D', 'E', 'F']:
            with self.subTest(
                    expected=self.PRIM_MST_EXPECTED[key],
                    actual=mst[key]):
                self.assertSetEqual(
                    set(self.PRIM_MST_EXPECTED[key]),
                    set(mst[key])
                )
