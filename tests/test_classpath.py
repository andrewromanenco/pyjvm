import unittest

from pyjvm.classpath import FolderClassPathEntry

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

if __name__ == '__main__':
    unittest.main()
