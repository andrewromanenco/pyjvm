import unittest

from pyjvm.utils.javap import javap
from pyjvm.utils.javap import ResolvedClass
from pyjvm.utils.javap import Field
from pyjvm.utils.javap import Method

class TestJavap(unittest.TestCase):

    def test_javap(self):
        resolved_class = javap('tests/res/SampleClass.class')
        self.assertEqual(
            resolved_class,
            ResolvedClass(
                accessor=['public'],
                class_or_interface='class',
                class_name='sample.pckg.SampleClass',
                interfaces=['java.io.Serializable'],
                fields=[
                    Field(flags=['private', 'static', 'final'], name='serialVersionUID', type='long'),
                    Field(flags=['protected', 'static', 'final'], name='value1', type='int'),
                    Field(flags=['static', 'final'], name='value2', type='double'),
                    Field(flags=['final'], name='value3', type='int'),
                    Field(flags=[], name='value4', type='int'),
                    Field(flags=[], name='value5', type='int[]')],
                methods=[
                    Method(flags=['static'], name='<clinit>', params=[], returns='void'),
                    Method(flags=['public', 'static'], name='main', params=['java.lang.String[]'], returns='void'),
                    Method(flags=['public'], name='<init>', params=[], returns='void'),
                    Method(flags=['public'], name='<init>', params=['int'], returns='void'),
                    Method(flags=['public'], name='apply', params=['java.util.function.Function'], returns='int'),
                    Method(flags=['private', 'static'], name='lambda$0', params=['java.lang.Integer'], returns='java.lang.Integer')]
                )
            )

if __name__ == '__main__':
    unittest.main()
