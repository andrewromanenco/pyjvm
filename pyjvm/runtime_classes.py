'''Runtime classes.'''

from pyjvm.utils.javap import resolve_class_name, resolve_super_class_name, resolve_interfaces


class RuntimeClass:
    '''Runtime version of a java class.'''

    def __init__(self, java_class):
        '''Init with a java class.'''
        self.__java_class = java_class
        self.__name = None

    def get_name(self):
        '''Return java binary class name. This is a string.'''
        if self.__name is not None:
            return self.__name
        self.__name = resolve_class_name(self.__java_class)
        return self.__name

    def get_super_name(self):
        '''Return super's java binary class name. This is a string. None for
        java/lang/Object'''
        if self.get_name() == 'java/lang/Object':
            return None
        return resolve_super_class_name(self.__java_class)

    def get_interface_names(self):
        '''Returns list of binary names if implemented interfaces.'''
        return resolve_interfaces(self.__java_class)
