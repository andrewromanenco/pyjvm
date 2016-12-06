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

    def test_get_super_name(self):
        self.assertEqual('java/lang/Object',
                         self.runtime_class.get_super_name())

    def test_get_interface_names(self):
        self.assertEqual(['java/io/Serializable'],
                         self.runtime_class.get_interface_names())

    def test_get_static_fields_definitions(self):
        self.assertEqual([('serialVersionUID', 'long'), ('value1', 'int'), (
            'value2', 'double')],
                         self.runtime_class.get_static_fields_definitions())


if __name__ == '__main__':
    unittest.main()
