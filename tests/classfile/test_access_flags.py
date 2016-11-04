import unittest

from pyjvm.classfile.access_flags import FlagSetBuilder

class TestFlagSetBuilder(unittest.TestCase):

    def test_build(self):
        testee = FlagSetBuilder()
        result = testee.set("A").set("B").build()
        self.assertTrue(result.is_set("A"))
        self.assertTrue(result.is_set("B"))
        self.assertFalse(result.is_set("C"))


if __name__ == '__main__':
    unittest.main()
