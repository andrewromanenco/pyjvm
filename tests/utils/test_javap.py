import unittest

from pyjvm.utils.javap import javap
from pyjvm.utils.javap import ResolvedClass
from pyjvm.utils.javap import Field

class TestJavap(unittest.TestCase):

    def test_javap(self):
        resolved_class = javap('tests/res/SampleClass.class')
        self.assertEqual(
            resolved_class,
            ResolvedClass(
                accessor=['public'],
                class_or_interface='class',
                class_name='sample/pckg/SampleClass',
                interfaces=['java/io/Serializable'],
                fields=[
                    Field(flags=['private', 'static', 'final'], name='serialVersionUID', type='long'),
                    Field(flags=['protected', 'static', 'final'], name='value1', type='int'),
                    Field(flags=['static', 'final'], name='value2', type='double'),
                    Field(flags=['final'], name='value3', type='int'),
                    Field(flags=[], name='value4', type='int'),
                    Field(flags=[], name='value5', type='int[]')]
                )
            )

if __name__ == '__main__':
    unittest.main()
