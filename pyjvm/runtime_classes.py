'''Runtime classes.'''

from collections import namedtuple
from pyjvm.utils.javap import resolve_class_name, resolve_super_class_name, resolve_interfaces, resolve_fields


class RuntimeClass:
    '''Runtime version of a java class.'''

    def __init__(self, java_class):
        '''Init with a java class.'''
        self.__java_class = java_class
        self.__name = None
        self.__static_fields = {}

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

    def get_static_fields_definitions(self):
        '''Return list of static fileds (name, type).'''
        all_fields = resolve_fields(self.__java_class)
        result = []
        Field = namedtuple('Field', ['name', 'type'])

        for field in all_fields:
            if 'static' in field.flags:
                result.append(Field(field.name, field.type))
        return result

    def set_field(name, value):
        self.__static_fields[name] = value

    def get_field(name):
        return self.__static_fields[name]
