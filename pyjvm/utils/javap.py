'''Resolves java class byte structures to human friendly strings.
Similar to javap decompiler'''
import struct

from collections import namedtuple

from pyjvm.bytecode_readers import BytecodeFileReader
from pyjvm.class_parser import ClassParser
from pyjvm.classfile.access_flags import ClassFlag
from pyjvm.classfile.access_flags import FieldFlag
from pyjvm.classfile.access_flags import MethodFlag

ResolvedClass = namedtuple('ResolvedClass', [
    'accessor', 'class_or_interface', 'class_name', 'super_class',
    'interfaces', 'fields', 'methods'
])

Field = namedtuple('Field', ['flags', 'name', 'type'])

Method = namedtuple('Method',
                    ['flags', 'name', 'params', 'returns', 'exceptions'])


def javap(path_to_bytecode):
    '''Expects a path to Java 8 class file and returns resolved strings.'''
    parser = ClassParser()
    klass = parser.parse(BytecodeFileReader(path_to_bytecode))
    resolved_class = ResolvedClass(
        accessor=resolve_class_accessor(klass),
        class_or_interface=resolve_class_or_interface(klass),
        class_name=resolve_class_name(klass).replace('/', '.'),
        super_class=resolve_super_class_name(klass).replace('/', '.'),
        interfaces=resolve_interfaces(klass),
        fields=resolve_fields(klass),
        methods=resolve_methods(klass))

    return resolved_class


def resolve_class_accessor(klass):
    '''Returns list of flags on a given class.'''
    result = []
    if klass.access_flags & ClassFlag.ACC_PUBLIC.value:
        result.append('public')
    if klass.access_flags & ClassFlag.ACC_ABSTRACT.value:
        result.append('abstract')
    if klass.access_flags & ClassFlag.ACC_FINAL.value:
        result.append('final')
    return result


def resolve_class_or_interface(klass):
    '''Decides if this is a class or an interface.'''
    if klass.access_flags & ClassFlag.ACC_INTERFACE.value:
        return 'interface'
    else:
        return 'class'


def resolve_class_name(klass):
    '''Resolves class name.'''
    return name_from_ConstantClassInfo(klass.constant_pool, klass.this_index)


def resolve_super_class_name(klass):
    '''Resolves super class name.'''
    return name_from_ConstantClassInfo(klass.constant_pool, klass.super_index)


def resolve_interfaces(klass):
    '''Returns list of all interfaces implemented by a given class.'''
    result = []
    for index in klass.interface_indexes:
        result.append(
            name_from_ConstantClassInfo(klass.constant_pool, index).replace(
                '/', '.'))
    return result


def resolve_fields(klass):
    '''Resolve all fields.'''
    result = []
    for field in klass.fields:
        name_entry = klass.constant_pool.entry(field.name_index)
        type_entry = klass.constant_pool.entry(field.descriptor_index)
        result.append(
            Field(
                flags=resolve_field_flags(field.access_flags),
                name=string_from_ConstantUtf8Info(name_entry),
                type=resolve_type(type_entry)))
    return result


def resolve_methods(klass):
    result = []
    for method in klass.methods:
        name_entry = klass.constant_pool.entry(method.name_index)
        type_entry = klass.constant_pool.entry(method.descriptor_index)
        params, returns = parse_signature(
            string_from_ConstantUtf8Info(type_entry))
        result.append(
            Method(
                flags=resolve_method_flags(method.access_flags),
                name=string_from_ConstantUtf8Info(name_entry),
                params=params,
                returns=returns,
                exceptions=resolve_exceptions(klass.constant_pool, method)))
    return result


def resolve_field_flags(access_flags):
    '''Decode flags.'''
    result = []
    if access_flags & FieldFlag.ACC_PUBLIC.value:
        result.append('public')
    if access_flags & FieldFlag.ACC_PRIVATE.value:
        result.append('private')
    if access_flags & FieldFlag.ACC_PROTECTED.value:
        result.append('protected')
    if access_flags & FieldFlag.ACC_STATIC.value:
        result.append('static')
    if access_flags & FieldFlag.ACC_FINAL.value:
        result.append('final')
    if access_flags & FieldFlag.ACC_VOLATILE.value:
        result.append('volatile')
    if access_flags & FieldFlag.ACC_TRANSIENT.value:
        result.append('transient')
    return result


def resolve_method_flags(access_flags):
    '''Decode flags.'''
    result = []
    if access_flags & MethodFlag.ACC_PUBLIC.value:
        result.append('public')
    if access_flags & MethodFlag.ACC_PRIVATE.value:
        result.append('private')
    if access_flags & MethodFlag.ACC_PROTECTED.value:
        result.append('protected')
    if access_flags & MethodFlag.ACC_STATIC.value:
        result.append('static')
    if access_flags & MethodFlag.ACC_FINAL.value:
        result.append('final')
    if access_flags & MethodFlag.ACC_SYNCHRONIZED.value:
        result.append('syncronized')
    if access_flags & MethodFlag.ACC_NATIVE.value:
        result.append('native')
    if access_flags & MethodFlag.ACC_ABSTRACT.value:
        result.append('abstract')
    return result


def resolve_exceptions(constant_pool, method):
    '''Read exception thrown by a method.'''
    result = []
    for attr in method.attributes:
        name = string_from_ConstantUtf8Info(
            constant_pool.entry(attr.attribute_name_index))
        if name == 'Exceptions':
            data = attr.info
            count = (data[0] << 8) + data[1]
            index = 2
            while count > 0:
                exception_name_index = (data[index] << 8) + data[index + 1]
                exception_name = name_from_ConstantClassInfo(
                    constant_pool, exception_name_index)
                result.append(exception_name.replace('/', '.'))
                index += 2
                count -= 1
    return result


def resolve_type(type_entry):
    '''Get field type.'''
    type_name = string_from_ConstantUtf8Info(type_entry)
    return unpack_type(type_name)


def unpack_type(type_name):
    '''Make type string uman friendly.'''
    if type_name[0] == '[':
        return unpack_type(type_name[1:]) + '[]'
    if type_name[0] == 'L':
        return type_name[1:-1].replace('/', '.')
    types = {
        'B': 'byte',
        'C': 'char',
        'D': 'double',
        'F': 'float',
        'I': 'int',
        'J': 'long',
        'S': 'short',
        'Z': 'boolean',
        'V': 'void'
    }
    return types[type_name]


def name_from_ConstantClassInfo(constant_pool, entry_index):
    '''Resolves specific entry from a constant pool.'''
    name_index = constant_pool.entry(entry_index).name_index
    return string_from_ConstantUtf8Info(constant_pool.entry(name_index))


def string_from_ConstantUtf8Info(entry):
    '''Resolves specific entry from a constant pool.'''
    return decode_utf8(entry.bytes)


def parse_signature(signature):
    signature = signature[1:]
    params = []
    while signature[0] != ')':
        token = read_next_token(signature)
        params.append(unpack_type(token))
        signature = signature[len(token):]
    returns = unpack_type(signature[1:])
    return (params, returns)


def read_next_token(signature):
    index = 0
    while signature[index] == '[':
        index += 1
    if signature[index] == 'L':
        return signature[:signature.index(';') + 1]
    else:
        return signature[:index + 1]


def decode_utf8(data):
    '''Decode bytes to UTF8 string.'''
    index = 0
    value = ""
    while index < len(data):
        c = struct.unpack(">B", bytes([data[index]]))[0]
        if (c >> 7) == 0:
            value += chr(c)
            index += 1
        elif (c >> 5) == 0b110:
            b = ord(data[index + 1])
            assert b & 0x80
            c = ((c & 0x1f) << 6) + (b & 0x3f)
            value += chr(c)
            index += 2
        elif (c >> 4) == 0b1110:
            y = ord(data[index + 1])
            z = ord(data[index + 2])
            c = ((c & 0xf) << 12) + ((y & 0x3f) << 6) + (z & 0x3f)
            value += chr(c)
            index += 3
        elif c == 0b11101101:
            v = ord(data[index + 1])
            w = ord(data[index + 2])
            # x = ord(data[index + 3]) No need this is marker
            y = ord(data[index + 4])
            z = ord(data[index + 5])
            c = 0x10000 + ((v & 0x0f) << 16) + ((w & 0x3f) << 10) \
                + ((y & 0x0f) << 6) + (z & 0x3f)
            value += chr(c)
            index += 6
        else:
            raise Exception("UTF8 is not fully implemented {0:b}".format(c))
    return value
