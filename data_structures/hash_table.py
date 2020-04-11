import unittest


class HashItem(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"{self.key}: {self.value}"


class HashTable(object):
    """Implementation of a HashTable using chaining; that means that in each
    array slot there is a list.
    """

    SIZE = 1024

    def __init__(self):
        self._slots = [list() for _ in range(self.SIZE)]

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    @classmethod
    def _hash(cls, key):
        """Hashing of the key. I decided to use the builtin hash function.
        I don't think I could think about something smarter and more efficient
        (in a general case) than C-implemented hashing function.

        To make sure that we end up with a value within our _slots size I added
        modulo `self.SIZE`.

        """
        return hash(key) % cls.SIZE

    def set(self, key, value):
        """Sets the key with value. If key already exists in dict it item is
        updated otherwise added.

        :param key: key
        :type key: object
        :param value: value
        :type value: object

        :Example:
        >>> hash_table = HashTable()
        >>> hash_table.set("It's dangerous to go alone...", "Take this!")
        >>> # The same functionality can be implemented with brackets:
        >>> # hash_table["It's dangerous to go alone..."] =  "Take this!"
        >>> hash_table["It's dangerous to go alone..."]
        "Take this!"
        """
        new_item = HashItem(key, value)
        index = self._hash(key)
        for iter_item in self._slots[index]:
            if iter_item.key == key:
                iter_item.value = value
                return
        self._slots[index].append(new_item)

    def get(self, key):
        """Gets the value of element saved with key.
        If key is not in the HashTable raises KeyError.

        :param key: key
        :type key: object
        :return: value
        :rtype: object
        :raises: KeyError

        :Example:
        >>> hash_table = HashTable()
        >>> hash_table["It's dangerous to go alone..."] =  "Take this!"
        >>> hash_table.get("It's dangerous to go alone...")
        >>> # The same functionality can be implemented with brackets:
        >>> # hash_table["It's dangerous to go alone..."]
        "Take this!"
        """
        index = self._hash(key)
        for iter_item in self._slots[index]:
            if iter_item.key == key:
                return iter_item.value
        raise KeyError(f"{key} is not in the hash table.")


class TestHashTable(unittest.TestCase):
    def test_init(self):
        hash_table = HashTable()
        self.assertListEqual([list()] * 1024, hash_table._slots)

    def test_hash(self):
        """I am not going to test builtin hash function. Just make sure it
        never exceeds `self.SIZE`.
        """
        test_input = [1, 2, 1023, 1024, 231312]
        expected = [1, 2, 1023, 0, 912]
        actual = [HashTable._hash(i) for i in test_input]
        for e, a in zip(expected, actual):
            with self.subTest(e=e, a=a):
                self.assertEqual(e, a)

    def test_put_one_element(self):
        hash_table = HashTable()
        hash_table.set(1, 'xyz')
        self.assertEqual(hash_table._slots[1][0].value, 'xyz')

    def test_put_update_element(self):
        hash_table = HashTable()
        hash_table.set(1, 'xyz')
        hash_table.set(1, 'abc')
        with self.subTest():
            self.assertEqual('abc', hash_table._slots[1][0].value)
        with self.subTest():
            self.assertEqual(1, len(hash_table._slots[1]))

    def test_put_multiple_elements(self):
        hash_table = HashTable()
        hash_table.set(1, 'xyz')
        hash_table.set(1025, 'abc')
        hash_table.set(2049, 'lol')
        actual = hash_table._slots[1]
        for e, a in zip(['xyz', 'abc', 'lol'], actual):
            with self.subTest(e=e, a=a.value):
                self.assertEqual(e, a.value)
        actual_len = len(hash_table._slots[1])
        expected_len = 3
        with self.subTest(e=expected_len, a=actual_len):
            self.assertEqual(expected_len, actual_len)

    def test_get_raises(self):
        hash_table = HashTable()
        with self.assertRaises(KeyError):
            _ = hash_table.get('xyz')

    def test_get_one_elem_in_slot(self):
        hash_table = HashTable()
        hash_table.set(1025, 'abc')
        self.assertEqual('abc', hash_table.get(1025))

    def test_get_multiple_elem_in_slot(self):
        hash_table = HashTable()
        hash_table.set(1, 'xyz')
        hash_table.set(1025, 'abc')
        hash_table.set(2049, 'lol')
        self.assertEqual('abc', hash_table.get(1025))

    def test_brackets(self):
        hash_table = HashTable()
        hash_table['You only'] = 'test once'
        self.assertEqual('test once', hash_table['You only'])

