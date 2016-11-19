import unittest

from pyjvm.classfile.constant_pool import ConstantPool
from pyjvm.classfile.constant_pool import ConstantPoolBuilder


class TestConstantPoolBuilder(unittest.TestCase):
    def test_add_entry(self):
        testee = ConstantPoolBuilder()
        testee.append_entry(1)
        pool = testee.build()
        self.assertTrue(isinstance(pool, ConstantPool))
        self.assertEqual(pool.entry(1), 1)

    def test_add_double_entry(self):
        testee = ConstantPoolBuilder()
        testee.append_double_entry(1)
        pool = testee.build()
        self.assertTrue(isinstance(pool, ConstantPool))
        self.assertEqual(pool.entry(1), 1)
        self.assertEqual(pool.entry(2), "EMPTY SPOT")


if __name__ == '__main__':
    unittest.main()
