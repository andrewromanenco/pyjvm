import unittest

from pyjvm.bytecode_readers import AbstractBytecodeReader
from pyjvm.bytecode_readers import BytecodeFileReader
from pyjvm.class_parser import ClassParser

class ListByteCodeReader(AbstractBytecodeReader):

    def __init__(self, data):
        self.bytes = bytes(data)
        self.index = 0

    def read(self, n):
        self.index += n
        if n == 1:
            return self.bytes[self.index - 1:self.index]
        else:
            return self.bytes[self.index - n: self.index]

    def size(self):
        return len(self.bytes)


class TestClassParser(unittest.TestCase):

    def setUp(self):
        self.parser = ClassParser()

    def test_parse_fails_when_not_valid_bytecode(self):
        with self.assertRaises(Exception) as context:
            self.parser.parse(ListByteCodeReader([0x00, 0x00, 0x00, 0x00]))
        self.assertTrue('No CAFEBABE' in str(context.exception))

    def test_parse_does_not_fail_with_good_input(self):
        self.parser.parse(BytecodeFileReader('tests/res/ArraysTest.class'))

if __name__ == '__main__':
    unittest.main()
