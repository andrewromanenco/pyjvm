'''Runtime classes.'''

from pyjvm.utils.javap import resolve_class_name


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
