import unittest

from pyjvm.classfile.constant_pool import ConstantPool


class TestConstantPoolBuilder(unittest.TestCase):
    def test_read_entry(self):
        testee = ConstantPool([1, 2])
        self.assertEqual(testee.entry(1), 1)
        self.assertEqual(testee.entry(2), 2)


if __name__ == '__main__':
    unittest.main()
