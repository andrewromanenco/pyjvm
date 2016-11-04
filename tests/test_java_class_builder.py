import unittest

from pyjvm.java_class import JavaClassBuilder

STUB = "stub"

class TestJavaClassBuilder(unittest.TestCase):

    def test_fail_if_no_constant_pool(self):
        testee = JavaClassBuilder()
        with self.assertRaises(Exception) as context:
            testee.with_access_flags(STUB).build()
        self.assertTrue('Constant pool is not provided' in str(context.exception))

    def test_fail_if_no_access_flags(self):
        testee = JavaClassBuilder()
        with self.assertRaises(Exception) as context:
            testee.with_constant_pool(STUB).build()
        self.assertTrue('Access flags are not provided' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
