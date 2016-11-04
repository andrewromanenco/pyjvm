import unittest

from pyjvm.java_class import JavaClassBuilder

class TestJavaClassBuilder(unittest.TestCase):

    def test_fail_if_no_constant_pool(self):
        testee = JavaClassBuilder()
        with self.assertRaises(Exception) as context:
            testee.build()
        self.assertTrue('Constant pool is not provided' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
