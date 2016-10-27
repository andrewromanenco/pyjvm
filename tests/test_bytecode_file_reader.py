import unittest

from pyjvm.bytecode_readers import BytecodeFileReader

class TestBytecodeFileReader(unittest.TestCase):

    def setUp(self):
        self.reader = BytecodeFileReader('tests/res/ArraysTest.class')

    def test_size_returns_all_bytes(self):
        self.assertEqual(self.reader.size(), 2924)

    def test_read_one_byte(self):
        byte = self.reader.read(1)
        self.assertTrue(isinstance(byte, bytes))
        self.assertEqual(len(byte), 1)
        self.assertEqual(byte[0], 0xCA)

    def test_read_only_available_bytes(self):
        byte = self.reader.read(5000)
        self.assertEqual(len(byte), 2924)

if __name__ == '__main__':
    unittest.main()
