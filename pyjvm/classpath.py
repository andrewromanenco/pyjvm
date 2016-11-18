'''Hande java class path and caches java classes names.'''

import os
import zipfile
from abc import ABCMeta, abstractmethod
from pyjvm.bytecode_readers import BytecodeFileReader, JarBytecodeFileReader

class ClassPath:
    '''Collection of class path entries.'''

    def __init__(self):
        '''Init new class path.'''
        self.entries = []

    def add(self, path):
        '''Path to a folder or a jar file.'''
        if os.path.isdir(path):
            self.entries.append(FolderClassPathEntry(path))
        else:
            self.entries.append(JarClassPathEntry(path))

    def bytes(self, class_name):
        '''Returns bytes for requested java binary name. None if not found.'''
        for entry in self.entries:
            data = entry.bytes(class_name)
            if data is not None:
                return data
        return None

class ClassPathEntry(metaclass=ABCMeta):
    '''An entry to in a class path.'''

    @abstractmethod
    def bytes(self, class_name):
        '''Returns bytes for requested java binary name. None if not found.'''
        pass


class FolderClassPathEntry(ClassPathEntry):
    '''Class path entry for a folder.'''

    def __init__(self, path_to_folder):
        '''Init entry with a folder. Throws exception if not a valid path.'''
        if not os.path.isdir(path_to_folder):
            raise ValueError('Not a path to folder: ' + str(path_to_folder))
        self.path = path_to_folder

    def bytes(self, class_name):
        '''Returns bytes for requested java binary name. None if not found.'''
        file_path = os.path.join(self.path, class_name + '.class')
        if not os.path.isfile(file_path):
            return None
        reader = BytecodeFileReader(file_path)
        return reader.read(reader.size())


class JarClassPathEntry(ClassPathEntry):
    '''Class path entry for a jar.'''

    def __init__(self, path_to_jar):
        '''Entry caches names of files in a jar. Throws exception on jar read
        error.'''
        if not os.path.isfile(path_to_jar):
            raise ValueError('No such file: ' + str(path_to_jar))
        self.path = path_to_jar
        self.classes = set()
        self.__cache_names_from_jar(path_to_jar)

    def __cache_names_from_jar(self, path_to_jar):
        with zipfile.ZipFile(path_to_jar, 'r') as zfile:
            for name in zfile.namelist():
                if name.endswith('.class'):
                    self.classes.add(name[:-6])

    def bytes(self, class_name):
        '''Returns bytes for requested java binary name. None if not found.'''
        if class_name not in self.classes:
            return None
        reader = JarBytecodeFileReader(self.path, class_name)
        return reader.read(reader.size())
