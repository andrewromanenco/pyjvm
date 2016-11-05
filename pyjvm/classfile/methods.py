"""Class methods."""

from collections import namedtuple
from pyjvm.classfile.attributes import read_attributes

Method = namedtuple(
    'Method',
    ['access_flags', 'name_index', 'descriptor_index', 'attributes_count', 'attributes'])

def read_methods(reader):
    """Read class methods."""
    methods_count = reader.get_u2()
    methods = []
    while methods_count > 0:
        access_flags = reader.get_u2()
        name_index = reader.get_u2()
        descriptor_index = reader.get_u2()
        attributes = read_attributes(reader)
        methods.append(Method(
            access_flags,
            name_index,
            descriptor_index,
            len(attributes),
            attributes
            ))
        methods_count -= 1
    return methods
