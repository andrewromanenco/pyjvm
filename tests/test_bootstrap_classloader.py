import unittest

from pyjvm.bootstrap_classloader import BootstrapClassloader
from pyjvm.classpath import ClassPath


class TestBootstrapClassloader(unittest.TestCase):
    def test_load_class(self):
        classpath = ClassPath()
        classpath.add('tests/res/sample.jar')
        testee = BootstrapClassloader(classpath)
        runtime_class = testee.load_class('some/pkg/JarredClass')
        self.assertIsNotNone(runtime_class)
        self.assertEqual('some/pkg/JarredClass', runtime_class.get_name())


if __name__ == '__main__':
    unittest.main()
