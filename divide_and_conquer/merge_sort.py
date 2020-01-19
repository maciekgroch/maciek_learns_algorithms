import unittest


def merge_sort(z, merge_algo='recursive'):
    """
    Implementation of merge_sort algorithm: For details please visit:
    https://en.wikipedia.org/wiki/Merge_sort

    :param z: unsorted array
    :type z: iterable
    :param merge_algo: two merge algorithms can be used `iterative` or `recursive`
    :type merge_algo: str
    :return: sorted array
    :type: list

    :Example:
    >>> z = [5, 3, 9, 1]
    >>> merge_sort(z)
    [1, 3, 5, 9]
    """
    n = len(z)
    if n == 1:
        return z
    left = z[:n//2]
    right = z[n//2:]
    if merge_algo == 'recursive':
        return _merge_recursive(merge_sort(left), merge_sort(right))
    elif merge_algo == 'iterative':
        return _merge_iterative(merge_sort(left), merge_sort(right))
    else:
        raise RuntimeError("Only 'recursive' and 'iterative' are allowed.")


def _merge_recursive(x, y):
    """
    Iteratively merges and sorts two arrays. Input arrays are expected to be
    sorted! Based on:
    Dasgupta, Sanjoy, Christos H. Papadimitriou, and Umesh V. Vazirani.
    *Algorithms*. Boston: McGraw-Hill Higher Education, 2008

    :param x: 1st array to be merged (must be sorted!)
    :type x: iterable
    :param y: 2nd array to be merged (must be sorted!)
    :type y: iterable
    :return: merged and sorted array of size len(x) + len(y)
    :rtype: list
    """
    n_x, n_y = len(x), len(y)
    if n_x == 0:
        return y
    if n_y == 0:
        return x
    if x[0] <= y[0]:
        return [x[0]] + _merge_recursive(x[1:], y)
    else:
        return [y[0]] + _merge_recursive(x, y[1:])


def _merge_iterative(x, y):
    """
    Iteratively merges and sorts two arrays. Input arrays must be sorted!
    Following the approach given in course:
    https://www.coursera.org/learn/algorithms-divide-conquer

    :param x: 1st of iterables to be merged (must be sorted!)
    :type x: iterable
    :param y: 2nd of iterables to be merged (must be sorted!)
    :type y: iterable
    :return: merged and sorted array of size len(x) + len(y)
    :rtype: list
    """
    n_x, n_y = len(x), len(y)
    i, j = 0, 0
    z = list()
    for k in range(n_x + n_y):
        if i == n_x:
            z += y[j:]
            break
        elif j == n_y:
            z += x[i:]
            break
        elif x[i] <= y[j]:
            z.append(x[i])
            i += 1
        else:
            z.append(y[j])
            j += 1
    return z


class TestMergeSort(unittest.TestCase):
    def test_merge_sort(self):
        input_set = [
            [1],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 3, 2, 4, 5, 6, 7, 8, 9],
            [1, 3, 4, 2, 5, 6, 7, 8, 9],
            [9, 8, 7, 6, 5, 4, 3, 2, 1],
            [2313, 2, 232, 1, 93, 0, 18]
        ]
        results = [sorted(i) for i in input_set]
        for algo in ['iterative', 'recursive']:
            for arr, result in zip(input_set, results):
                with self.subTest(arr=arr, result=result):
                    self.assertEqual(merge_sort(arr, algo), result)

    def test_merge_recursive(self):
        self._test_merge(_merge_recursive)

    def test_merge_iterative(self):
        self._test_merge(_merge_iterative)

    def _test_merge(self, merge):
        input_set = [
            ([], [1], [1]),
            ([1], [], [1]),
            ([], [], []),
            ([1], [1], [1, 1]),
            ([1, 2, 3], [2, 3, 4], [1, 2, 2, 3, 3, 4]),
            ([1000], [1, 2, 3], [1, 2, 3, 1000]),
            ([1, 2, 3], [1, 1, 1], [1, 1, 1, 1, 2, 3]),
        ]
        for left, right, expected in input_set:
            with self.subTest(left=left, right=right, expected=expected):
                result = merge(left, right)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
