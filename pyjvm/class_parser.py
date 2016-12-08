'''Parse java bytecode.'''

from pyjvm.java_class import JavaClassBuilder
from pyjvm.classfile.constant_pool import read_constant_pool
from pyjvm.classfile.interfaces import read_interfaces
from pyjvm.classfile.fields import read_fields
from pyjvm.classfile.methods import read_methods


class ClassParser:
    """Parse java bytecode to in-memory structure."""

    def parse(self, bytecode):
        """Read bytes from a source and create JavaClass instance. Bytecode is a list of bytes."""
        reader = _ByteReaderDecorator(bytecode)
        self.__confirm_header(reader)
        self.__confirm_jdk8(reader)
        constant_pool = read_constant_pool(reader)
        access_flags = reader.get_u2()
        this_class_index = reader.get_u2()
        super_class_index = reader.get_u2()
        interface_indexes = read_interfaces(reader)
        fields = read_fields(reader)
        methods = read_methods(reader)
        return JavaClassBuilder() \
            .with_constant_pool(constant_pool) \
            .with_access_flags(access_flags) \
            .with_this_class_index(this_class_index) \
            .with_super_class_index(super_class_index) \
            .with_interface_indexes(interface_indexes) \
            .with_fields(fields) \
            .with_methods(methods) \
            .build()

    def __confirm_header(self, reader):
        '''Valid bytecode must start with 0xCAFEBABE.'''
        cafebabe = [0xCA, 0xFE, 0xBA, 0xBE]
        index = 0
        while index < 4:
            byte = reader.get_u1()
            if byte != cafebabe[index]:
                raise Exception("No CAFEBABE")
            index += 1

    def __confirm_jdk8(self, reader):
        '''Make sure this is java 7 class'''
        reader.get_u2()
        major = reader.get_u2()
        if major != 0x34:  # 52 - jdk8
            raise Exception("Not a jdk8 class")


class _ByteReaderDecorator:
    '''Util class to make byte processing easier.'''

    def __init__(self, bytecode):
        '''Init with a valid BytecodeReader.'''
        self.bytecode = bytecode
        self.pointer = 0

    def get_u1(self):
        '''Read single byte.'''
        value = self.bytecode[self.pointer]
        self.pointer += 1
        return value

    def get_u2(self):
        '''Read two bytes.'''
        byte1 = self.bytecode[self.pointer]
        byte2 = self.bytecode[self.pointer + 1]
        self.pointer += 2
        return (byte1 << 8) + byte2

    def get_u4(self):
        '''Read four bytes.'''
        byte1 = self.bytecode[self.pointer]
        byte2 = self.bytecode[self.pointer + 1]
        byte3 = self.bytecode[self.pointer + 2]
        byte4 = self.bytecode[self.pointer + 3]
        self.pointer += 4
        return (byte1 << 24) + (byte2 << 16) + (byte3 << 8) + byte4

    def get_uv(self, length):
        '''Read variable amount of bytes.'''
        data = self.bytecode[self.pointer:self.pointer + length]
        self.pointer += length
        return data
