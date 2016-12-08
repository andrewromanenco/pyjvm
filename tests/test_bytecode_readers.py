import unittest

from pyjvm.bytecode_readers import bytecode_from_file, bytecode_from_jar


class TestBytecodeRead(unittest.TestCase):
    def test_bytecode_from_file(self):
        bytecode = bytecode_from_file('tests/res/SampleClass.class')
        self.assertTrue(isinstance(bytecode, bytes))
        self.assertEqual(len(bytecode), 1989)
        self.assertEqual(bytecode[0], 0xCA)

    def test_bytecode_from_jar(self):
        bytecode = bytecode_from_jar('tests/res/sample.jar',
                                     'some/pkg/JarredClass')
        self.assertEqual(len(bytecode), 205)
        self.assertEqual(bytecode[0], 0xCA)


if __name__ == '__main__':
    unittest.main()
