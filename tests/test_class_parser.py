import unittest

from pyjvm.bytecode_readers import bytecode_from_file
from pyjvm.class_parser import ClassParser
from pyjvm.classfile.access_flags import ClassFlag


class TestClassParser(unittest.TestCase):
    def setUp(self):
        self.parser = ClassParser()

    def test_parse_fails_when_not_valid_bytecode(self):
        with self.assertRaises(Exception) as context:
            self.parser.parse(bytes([0x00, 0x00, 0x00, 0x00]))
        self.assertTrue('No CAFEBABE' in str(context.exception))

    def test_parse_does_not_fail_with_good_input(self):
        klass = self.parser.parse(
            bytecode_from_file('tests/res/SampleClass.class'))
        self.assertEqual(klass.constant_pool.slots_count(), 110)
        self.assertTrue(klass.access_flags & ClassFlag.ACC_PUBLIC.value)
        self.assertFalse(klass.access_flags & ClassFlag.ACC_FINAL.value)
        self.assertEqual(klass.this_index, 1)
        self.assertEqual(klass.super_index, 21)
        self.assertEqual(len(klass.interface_indexes), 1)
        self.assertEqual(len(klass.fields), 6)
        self.assertEqual(len(klass.methods), 7)


if __name__ == '__main__':
    unittest.main()
