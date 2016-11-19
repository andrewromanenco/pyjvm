'''Runtime classes.'''

from pyjvm.utils.javap import resolve_class_name

class RuntimeClass:
    '''Runtime version of a java class.'''

    def __init__(self, java_class):
        '''Init with a java class.'''
        self.__java_class = java_class

    def get_name(self):
        '''Return java binary class name. This is a string.'''
        return resolve_class_name(self.__java_class)
