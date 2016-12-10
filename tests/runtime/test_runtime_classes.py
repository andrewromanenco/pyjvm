import unittest

from pyjvm.bytecode_readers import bytecode_from_file
from pyjvm.class_parser import ClassParser
from pyjvm.runtime.runtime_classes import RuntimeClass


class TestRuntimeClass(unittest.TestCase):
    def setUp(self):
        parser = ClassParser()
        bytecode = parser.parse(
            bytecode_from_file('tests/res/SampleClass.class'))
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
        self.assertEqual([('serialVersionUID', 'J'), ('value1', 'I'),
                          ('value2', 'D')],
                         self.runtime_class.get_static_fields_definitions())

    def test_get_method_none(self):
        method = self.runtime_class.get_method('no', '()V')
        self.assertIsNone(method)

    def test_get_method(self):
        method = self.runtime_class.get_method(
            'apply', '(Ljava/util/function/Function;)I')
        self.assertEqual('apply', method.get_name())
        self.assertEqual('(Ljava/util/function/Function;)I',
                         method.get_signature())


if __name__ == '__main__':
    unittest.main()
