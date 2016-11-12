import unittest

from pyjvm.utils.javap import javap
from pyjvm.utils.javap import ResolvedClass

class TestJavap(unittest.TestCase):

    def test_javap(self):
        resolved_class = javap('tests/res/SampleClass.class')
        self.assertEqual(
            resolved_class,
            ResolvedClass(
                accessor=['public'],
                class_or_interface='class',
                class_name='sample/pckg/SampleClass',
                interfaces=['java/io/Serializable']
                )
            )

if __name__ == '__main__':
    unittest.main()
