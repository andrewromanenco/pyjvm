import unittest

from pyjvm.bytecode_readers import BytecodeFileReader
from pyjvm.class_parser import ClassParser
from pyjvm.runtime_classes import RuntimeClass


class TestRuntimeClass(unittest.TestCase):
    def setUp(self):
        parser = ClassParser()
        bytecode = parser.parse(
            BytecodeFileReader('tests/res/SampleClass.class'))
        self.runtime_class = RuntimeClass(bytecode)

    def test_get_name(self):
        self.assertEqual('sample/pckg/SampleClass',
                         self.runtime_class.get_name())


if __name__ == '__main__':
    unittest.main()
