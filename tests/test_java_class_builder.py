import unittest

from pyjvm.java_class import JavaClassBuilder

STUB = "stub"

class TestJavaClassBuilder(unittest.TestCase):

    def test_fail_if_no_constant_pool(self):
        testee = JavaClassBuilder()
        with self.assertRaises(Exception) as context:
            testee \
                .with_access_flags(STUB) \
                .with_interface_indexes(STUB) \
                .with_fields(STUB) \
                .build()
        self.assertTrue('Constant pool is not provided' in str(context.exception))

    def test_fail_if_no_access_flags(self):
        testee = JavaClassBuilder()
        with self.assertRaises(Exception) as context:
            testee \
                .with_constant_pool(STUB) \
                .with_interface_indexes(STUB) \
                .with_fields(STUB) \
                .build()
        self.assertTrue('Access flags are not provided' in str(context.exception))

    def test_fail_if_no_interface_indexes(self):
        testee = JavaClassBuilder()
        with self.assertRaises(Exception) as context:
            testee \
                .with_constant_pool(STUB) \
                .with_access_flags(STUB) \
                .with_fields(STUB) \
                .build()
        self.assertTrue('Interface indexes were not set' in str(context.exception))

    def test_fail_if_no_fields(self):
        testee = JavaClassBuilder()
        with self.assertRaises(Exception) as context:
            testee \
                .with_constant_pool(STUB) \
                .with_access_flags(STUB) \
                .with_interface_indexes(STUB) \
                .build()
        self.assertTrue('Fields are not set' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
