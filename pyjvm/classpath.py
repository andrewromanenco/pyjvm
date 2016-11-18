'''Hande java class path and caches java classes names.'''

import os
from abc import ABCMeta, abstractmethod
from pyjvm.bytecode_readers import BytecodeFileReader

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
