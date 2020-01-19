import unittest


def multiply_karatsuba(x, y):
    """
    Multiplies two integers x and y using the Karatsuba algorithm:
    https://en.wikipedia.org/wiki/Karatsuba_algorithm

    :param x: 1st number
    :type x: int
    :param y: 2nd number
    :type y: int
    :return: result x*y
    :rtype: int

    :Example:
    >>> multiply_karatsuba(231231221, 49583412)
    11465232898106052
    """
    if type(x) != int or type(y) != int:
        raise ValueError('Only integers are supported!')
    x = str(x)
    y = str(y)
    n = max(len(x), len(y))
    i = n // 2
    if (n % 2) != 0:
        i += 1
    if len(x) == 1 and len(y) == 1:
        return int(x) * int(y)
    if len(x) < len(y):
        x = '0' * (len(y) - len(x)) + x
    elif len(y) < len(x):
        y = '0' * (len(x) - len(y)) + y
    a = int(x[:i])
    b = int(x[i:])
    c = int(y[:i])
    d = int(y[i:])
    ac = multiply_karatsuba(a, c)
    bd = multiply_karatsuba(b, d)
    z = multiply_karatsuba((a + b), (c + d)) - ac - bd
    return ac * 10**(2*(n-i)) + z * 10**(n-i) + bd


class TestMultiplyKaratsuba(unittest.TestCase):
    def test_multiply(self):
        test_set = [
            (2, 2, 4), (10, 10, 100), (232123, 231321, 53694924483),
            (123123123123123, 999299929992, 123036928317333210296405016)
        ]
        for x, y, result in test_set:
            with self.subTest(x=x, y=y, result=result):
                self.assertEqual(multiply_karatsuba(x, y), result)

    def test_raises(self):
        test_set = [(2, 9.1), (3.1, 2), (1.1, 2.2)]
        for x, y in test_set:
            with self.subTest(x=x, y=y):
                with self.assertRaises(ValueError):
                    multiply_karatsuba(x, y)


if __name__ == '__main__':
    unittest.main()
