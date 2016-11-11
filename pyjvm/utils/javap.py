'''Resolves java class byte structures to human friendly strings.
Similar to javap decompiler'''
import struct

from collections import namedtuple

from pyjvm.bytecode_readers import BytecodeFileReader
from pyjvm.class_parser import ClassParser
from pyjvm.classfile.access_flags import AccessFlag

ResolvedClass = namedtuple(
    'ResolvedClass',
    ['accessor', 'class_or_interface', 'class_name', 'interfaces'])

def javap(path_to_bytecode):
    '''Expects a path to Java 8 class file and returns resolved strings.'''
    parser = ClassParser()
    klass = parser.parse(BytecodeFileReader(path_to_bytecode))
    resolved_class = ResolvedClass(
        accessor=resolve_class_accessor(klass),
        class_or_interface=resolve_class_or_interface(klass),
        class_name=resolve_class_name(klass),
        interfaces=resolve_interfaces(klass)
        )
    #print_class_declaration(resolved_class, klass)
    #print_class_fields(resolved_class, klass)
    #print_class_methods(resolved_class, klass)

    return resolved_class

def resolve_class_accessor(klass):
    '''Returns list of flags on a given class.'''
    result = []
    if klass.access_flags.is_set(AccessFlag.ACC_PUBLIC):
        result.append('public')
    if klass.access_flags.is_set(AccessFlag.ACC_ABSTRACT):
        result.append('abstract')
    if klass.access_flags.is_set(AccessFlag.ACC_FINAL):
        result.append('final')
    return result

def resolve_class_or_interface(klass):
    '''Decides if this is a class or an interface.'''
    if klass.access_flags.is_set(AccessFlag.ACC_INTERFACE):
        return 'interface'
    else:
        return 'class'

def resolve_class_name(klass):
    '''Resolves class name.'''
    return name_from_ConstantClassInfo(klass.constant_pool, klass.this_index)

def resolve_interfaces(klass):
    '''Returns list of all interfaces implemented by a given class.'''
    result = []
    for index in klass.interface_indexes:
        result.append(name_from_ConstantClassInfo(klass.constant_pool, index))
    return result

def name_from_ConstantClassInfo(constant_pool, entry_index):
    '''Resolves specific entry from a constant pool.'''
    name_index = constant_pool.entry(entry_index).name_index
    return string_from_ConstantUtf8Info(constant_pool.entry(name_index))

def string_from_ConstantUtf8Info(entry):
    '''Resolves specific entry from a constant pool.'''
    return decode_utf8(entry.bytes)

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
            raise Exception("UTF8 is not fully implemented {0:b}"
                            .format(c))
    return value
