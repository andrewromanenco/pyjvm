'''Parse java bytecode.'''

from pyjvm.java_class import JavaClassBuilder
from pyjvm.classfile.access_flags import read_access_flags
from pyjvm.classfile.constant_pool import read_constant_pool
from pyjvm.classfile.interfaces import read_interfaces
from pyjvm.classfile.fields import read_fields
from pyjvm.classfile.methods import read_methods

class ClassParser:
    """Parse java bytecode to in-memory structure."""

    def parse(self, bytecode_reader):
        """Read bytes from a source and create JavaClass instance."""
        reader = _ByteReaderDecorator(bytecode_reader)
        self.__confirm_header(reader)
        self.__confirm_jdk7(reader)
        constant_pool = read_constant_pool(reader)
        access_flags = read_access_flags(reader)
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

    def __confirm_jdk7(self, reader):
        '''Make sure this is java 7 class'''
        reader.get_u2()
        major = reader.get_u2()
        if major != 0x33:  # 52 - jdk7
            raise Exception("Not a jdk7 class")


class _ByteReaderDecorator:
    '''Util class to make byte processing easier.'''

    def __init__(self, bytecode_reader):
        '''Init with a valid BytecodeReader.'''
        self.reader = bytecode_reader

    def get_u1(self):
        '''Read single byte.'''
        return self.reader.read(1)[0]

    def get_u2(self):
        '''Read two bytes.'''
        byte1 = self.reader.read(1)[0]
        byte2 = self.reader.read(1)[0]
        return (byte1 << 8) + byte2

    def get_u4(self):
        '''Read four bytes.'''
        byte1 = self.reader.read(1)[0]
        byte2 = self.reader.read(1)[0]
        byte3 = self.reader.read(1)[0]
        byte4 = self.reader.read(1)[0]
        return (byte1 << 24) + (byte2 << 16) + (byte3 << 8) + byte4

    def get_uv(self, length):
        '''Read variable amount of bytes.'''
        data = self.reader.read(length)
        return data
