import unittest

import numpy as np


def quick_sort(z, l=0, r=None):
    """
    Implementation of the quicksort algorithm. For details please visit:
    https://en.wikipedia.org/wiki/Quicksort

    What requires further explanation is how the pivot is chosen. Quicksort
    oscillates between O(nlog) and O(n^2) -- choosing the right pivot helps
    ensure the best performance.

    In this implementation I follow what suggested in the online course I took:
    looking at the first, the middle, and the last element and choosing the
    median:
    Given that we have array: [5, 3, 2, 11, 32, 99, 7]
    We select three: [5, 11, 7]
    Median is selected: 7 and later used as pivot.

    Sorting is inplace! That means that the input is modified and None is
    returned.

    :param z: array to be sorted
    :type z: iterable
    :param l: index of the left border
    :type l: int
    :param r: index of the right border
    :type r: int

    :Example:
    >>> z = [5, 3, 9, 1]
    >>> quick_sort(z)
    >>> z
    [1, 3, 5, 9]
    """
    if r is None:
        r = len(z)
    if r - l <= 1:
        return
    i = partition_array(z, l, r)
    quick_sort(z, l, i)
    quick_sort(z, i + 1, r)


def partition_array(z, l, r):
    """
    Partitions array around pivot into three: | < p | p | > p |.
    Returns index of p

    :param z: input index (operation is inplace)
    :type z: iterable
    :param l: index of the left border
    :type l: int
    :param r: index of the right border
    :type r: int
    :return: index of the pivot
    :rtype: int

    Example:
    >>> z = [5, 3, 2, 11, 32, 99, 7]
    >>> partition_array(z, 0, len(z))
    3  # pivot (which in this case is 7 will be placed at index 3)
    >>> z
    [5, 3, 2, 7, 32, 99, 11]  # (all <7 are on the left side, >7 on the right)

    Another exakple --  here we would simulate the second execution on the left
    part of the array after the first partition has been executed:
    >>> z = [5, 3, 2, 11, 32, 99, 7]
    >>> _ = partition_array(z, 0, len(z))
    >>> _ = partition_array(z, 0, 3)
    >>> z
    [2, 3, 5, 7, 32, 99, 11]  # left part already sorted.

    """
    set_pivot_as_first(z, l, r)
    pivot = z[l]
    i = l + 1
    for j in range(l + 1, r):
        if z[j] < pivot:
            z[j], z[i] = z[i], z[j]
            i = i + 1
    z[l], z[i - 1] = z[i - 1], z[l]
    return i - 1


def set_pivot_as_first(z, l, r):
    """
    Chooses pivot.

    I follow what suggested in the online course I took:
    looking at the first, the middle, and the last element and choosing the
    median:
    Given that we have array: [5, 3, 2, 11, 32, 99, 7]
    We select three: [5, 11, 7]
    Median is selected: 7 and later used as pivot.

    :param z: array in which pivot is selected as first
    :type z: iterable
    :param l: index of the left border
    :type l: int
    :param r: index of the right border
    :type r: int
    """
    indexes = [l, (r-l-1)//2 + l, r-1]
    first, middle, last = [z[i] for i in indexes]
    pivot_index = np.argsort([first, middle, last])[1]  # the middle one
    z[l], z[indexes[pivot_index]] = z[indexes[pivot_index]], z[l]


class TestQuickSort(unittest.TestCase):
    def test_quick_sort(self):
        input_set = [
            [1],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 3, 2, 4, 5, 6, 7, 8, 9],
            [1, 3, 4, 2, 5, 6, 7, 8, 9],
            [9, 8, 7, 6, 5, 4, 3, 2, 1],
            [2313, 2, 232, 1, 93, 0, 18]
        ]
        results = [sorted(i) for i in input_set]
        for arr, result in zip(input_set, results):
            with self.subTest(arr=arr, result=result):
                l, r = 0, len(arr)
                quick_sort(arr, l, r)
                self.assertListEqual(arr, result)

    def test_partition_array(self):
        input_set = [
            ([3, 4, 5, 2, 1], [1, 2, 3, 4, 5], 2),
            ([9, 9, 2, 18, 33, 34], [2, 9, 9, 18, 33, 34], 1)
        ]
        for arr, expected_arr, expected_i in input_set:
            with self.subTest(
                    arr=arr, expected_arr=expected_arr, expected_i=expected_i):
                l, r = 0, len(arr)
                i = partition_array(arr, l, r)
                self.assertListEqual(arr, expected_arr)
                self.assertEqual(i, expected_i)

    def test_set_pivot_as_first(self):
        input_set = [
            ([3, 4, 5, 2, 1], 0, 5, 3,),
            ([9, 9, 2, 18, 33, 34], 0, 6, 9),
            ([9, 9, 2, 18, 33, 34], 0, 4, 9),
            ([11, 9, 2, 18, 33, 34], 0, 4, 11),
        ]
        for arr, l, r, median in input_set:
            with self.subTest(arr=arr, median=median):
                set_pivot_as_first(arr, l, r)
                self.assertEqual(arr[0], median)


if __name__ == '__main__':
    unittest.main()

