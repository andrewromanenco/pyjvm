'''Runtime classes.'''

from collections import namedtuple
from pyjvm.classfile.access_flags import FieldFlag
from pyjvm.utils.javap import resolve_class_name, resolve_super_class_name, resolve_interfaces, string_from_ConstantUtf8Info


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
        '''Return list of static fields (name, type).'''
        result = []
        Field = namedtuple('Field', ['name', 'type'])
        for field in self.__java_class.fields:
            if field.access_flags & FieldFlag.ACC_STATIC.value:
                name_entry = self.__java_class.constant_pool.entry(
                    field.name_index)
                type_entry = self.__java_class.constant_pool.entry(
                    field.descriptor_index)
                result.append(
                    Field(
                        name=string_from_ConstantUtf8Info(name_entry),
                        type=string_from_ConstantUtf8Info(type_entry)))
        return result

    def set_field(self, name, value):
        '''Set value for a static field.'''
        self.__static_fields[name] = value

    def get_field(self, name):
        '''Get a value for a static field defined in this class.'''
        return self.__static_fields[name]

    def get_method(self, method_name, method_signature):
        '''Returns method for given name and signature. Does not check parent.'''
        for method in self.__java_class.methods:
            name_entry = self.__java_class.constant_pool.entry(
                method.name_index)
            name = string_from_ConstantUtf8Info(name_entry)
            if name != method_name:
                continue
            type_entry = self.__java_class.constant_pool.entry(
                method.descriptor_index)
            signature = string_from_ConstantUtf8Info(type_entry)
            if signature != method_signature:
                continue
            return Method(name, signature, method)
        return None


class Method:
    '''A method.'''

    def __init__(self, name, signature, binary_method_structure):
        '''Init method data.'''
        self.name = name
        self.signature = signature

    def get_name(self):
        return self.name

    def get_signature(self):
        return self.signature
