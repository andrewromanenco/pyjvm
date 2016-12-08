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
        java_class = ClassParser().parse(bytecode)
        return RuntimeClass(java_class)
