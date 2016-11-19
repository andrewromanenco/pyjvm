import unittest

from pyjvm.classpath import ClassPath, FolderClassPathEntry, JarClassPathEntry


class TestClassPath(unittest.TestCase):
    def setUp(self):
        self.testee = ClassPath()

    def test_read_from_folder(self):
        self.testee.add('tests/res')
        self.testee.add('tests/res/sample.jar')
        data = self.testee.bytes('SampleClass')
        self.assertEqual(len(data), 1989)

    def test_read_from_jar(self):
        self.testee.add('tests/res')
        self.testee.add('tests/res/sample.jar')
        data = self.testee.bytes('some/pkg/JarredClass')
        self.assertEqual(len(data), 205)


class TestFolderClassPathEntry(unittest.TestCase):
    def test_fail_if_wrong_path(self):
        with self.assertRaises(ValueError) as context:
            FolderClassPathEntry('/non/existing/path/123')
        self.assertTrue('Not a path to folder: ' in str(context.exception))

    def test_works_with_right_path(self):
        FolderClassPathEntry('tests/res')

    def test_bytes_none_if_no_class(self):
        entry = FolderClassPathEntry('tests/res')
        data = entry.bytes('NoClass')
        self.assertIsNone(data)

    def test_bytes_for_class(self):
        entry = FolderClassPathEntry('tests/res')
        data = entry.bytes('SampleClass')
        self.assertEqual(len(data), 1989)


class TestJarClassPathEntry(unittest.TestCase):
    def test_fail_if_wrong_path(self):
        with self.assertRaises(ValueError) as context:
            JarClassPathEntry('/non/existing/path/123')
        self.assertTrue('No such file: ' in str(context.exception))

    def test_fail_if_not_a_jar(self):
        with self.assertRaises(Exception) as context:
            JarClassPathEntry('tests/res/SampleClass.class')
        self.assertTrue('File is not a zip file' in str(context.exception))

    def test_works_with_right_path(self):
        JarClassPathEntry('tests/res/sample.jar')

    def test_bytes_none_if_no_class(self):
        entry = JarClassPathEntry('tests/res/sample.jar')
        data = entry.bytes('NoClass')
        self.assertIsNone(data)

    def test_bytes_for_class(self):
        entry = JarClassPathEntry('tests/res/sample.jar')
        data = entry.bytes('some/pkg/JarredClass')
        self.assertEqual(len(data), 205)


if __name__ == '__main__':
    unittest.main()
