"""Constant pool related code."""

from collections import namedtuple
from enum import Enum

class Tag(Enum):
    """Constant pool tags."""

    CONSTANT_Class = 7
    CONSTANT_Fieldref = 9
    CONSTANT_Methodref = 10
    CONSTANT_InterfaceMethodref = 11
    CONSTANT_String = 8
    CONSTANT_Integer = 3
    CONSTANT_Float = 4
    CONSTANT_Long = 5
    CONSTANT_Double = 6
    CONSTANT_NameAndType = 12
    CONSTANT_Utf8 = 1
    CONSTANT_MethodHandle = 15
    CONSTANT_MethodType = 16

# These are definitions from Jvm8 specs; Chapter 4.4
ConstantClassInfo = namedtuple(
    'ConstantClassInfo',
    ['name_index'])

ConstantStringInfo = namedtuple(
    'ConstantStringInfo',
    ['string_index'])

ConstantNameAndTypeInfo = namedtuple(
    'ConstantNameAndTypeInfo',
    ['name_index', 'descriptor_index'])

ConstantFieldrefInfo = namedtuple(
    'ConstantFieldrefInfo',
    ['class_index', 'name_and_type_index'])

ConstantMethodrefInfo = namedtuple(
    'ConstantMethodrefInfo',
    ['class_index', 'name_and_type_index'])

ConstantInterfaceMethodrefInfo = namedtuple(
    'ConstantInterfaceMethodrefInfo',
    ['class_index', 'name_and_type_index'])

ConstantLongInfo = namedtuple(
    'ConstantLongInfo',
    ['high_bytes', 'low_bytes'])

ConstantDoubleInfo = namedtuple(
    'ConstantDoubleInfo',
    ['high_bytes', 'low_bytes'])

ConstantFloatInfo = namedtuple(
    'ConstantFloatInfo',
    ['bytes'])

ConstantUtf8Info = namedtuple(
    'ConstantUtf8Info',
    ['length', 'bytes'])

def read_constant_pool(reader):
    """Parse constant pool entries from a stream."""
    cp_size = reader.get_u2()
    builder = ConstantPoolBuilder()
    while cp_size > 1:
        cp_entry_type = reader.get_u1()
        if cp_entry_type == Tag.CONSTANT_Fieldref.value:
            builder.append_entry(
                ConstantFieldrefInfo(
                    class_index=reader.get_u2(),
                    name_and_type_index=reader.get_u2()))
        elif cp_entry_type == Tag.CONSTANT_Methodref.value:
            builder.append_entry(
                ConstantMethodrefInfo(
                    class_index=reader.get_u2(),
                    name_and_type_index=reader.get_u2()))
        elif cp_entry_type == Tag.CONSTANT_InterfaceMethodref.value:
            builder.append_entry(
                ConstantInterfaceMethodrefInfo(
                    class_index=reader.get_u2(),
                    name_and_type_index=reader.get_u2()))
        elif cp_entry_type == Tag.CONSTANT_Class.value:
            builder.append_entry(
                ConstantClassInfo(
                    name_index=reader.get_u2()))
        elif cp_entry_type == Tag.CONSTANT_Long.value:
            cp_size -= 1
            builder.append_double_entry(
                ConstantLongInfo(
                    high_bytes=reader.get_u4(),
                    low_bytes=reader.get_u4()))
        elif cp_entry_type == Tag.CONSTANT_Double.value:
            cp_size -= 1
            builder.append_double_entry(
                ConstantDoubleInfo(
                    high_bytes=reader.get_u4(),
                    low_bytes=reader.get_u4()))
        elif cp_entry_type == Tag.CONSTANT_Float.value:
            builder.append_entry(
                ConstantFloatInfo(
                    bytes=reader.get_u4()))
        elif cp_entry_type == Tag.CONSTANT_String.value:
            builder.append_entry(
                ConstantStringInfo(
                    string_index=reader.get_u2()))
        elif cp_entry_type == Tag.CONSTANT_Utf8.value:
            utf8_length = reader.get_u2()
            utf8_bytes = reader.get_uv(utf8_length)
            builder.append_entry(
                ConstantUtf8Info(
                    length=utf8_length,
                    bytes=utf8_bytes))
        elif cp_entry_type == Tag.CONSTANT_NameAndType.value:
            builder.append_entry(
                ConstantNameAndTypeInfo(
                    name_index=reader.get_u2(),
                    descriptor_index=reader.get_u2()))
        else:
            raise Exception("Not supported entry type: %d" % cp_entry_type)
        cp_size -= 1
    return builder.build()

class ConstantPoolBuilder:
    """Build constant pool."""

    def __init__(self):
        """Init with no entries."""
        self.entries = []

    def append_entry(self, entry):
        """Add an entry."""
        self.entries.append(entry)

    def append_double_entry(self, entry):
        """Add an entry taking two spots in the list."""
        self.entries.append(entry)
        self.entries.append("EMPTY SPOT")

    def build(self):
        """Return constructed constant pool."""
        return ConstantPool(self.entries)

class ConstantPool:
    """Constant pool."""

    def __init__(self, entries):
        """Init pool with given entries."""
        self.entries = entries

    def entry(self, index):
        """Return an entry by index."""
        return self.entries[index - 1]

    def slots_count(self):
        """Returns number of slots in the pool. Not same as number of items."""
        return len(self.entries)
