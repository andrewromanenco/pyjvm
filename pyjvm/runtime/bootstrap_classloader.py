'''VM class loaders.'''

from pyjvm.class_parser import ClassParser
from pyjvm.runtime.runtime_classes import RuntimeClass


class BootstrapClassloader():
    '''VM bootstrap class loader.'''

    def __init__(self, classpath):
        '''Init with a classpath.'''
        self.classpath = classpath

    def load_class(self, class_name):
        '''Get runtime class for a given binary class name.'''
        bytecode = self.classpath.bytes(class_name)
        if bytecode is None:
            raise Exception('No such class ' + class_name)
        java_class = ClassParser().parse(_BytesToStream(bytecode))
        return RuntimeClass(java_class)


class _BytesToStream:
    '''Temp class. To be refactored out.'''

    def __init__(self, data_bytes):
        '''Init with bytes.'''
        self.__data = data_bytes
        self.__pointer = 0

    def read(self, num_of_bytes):
        '''Read bytes from pointer and move the pointer.'''
        result = self.__data[self.__pointer:self.__pointer + num_of_bytes]
        self.__pointer += num_of_bytes
        return result
