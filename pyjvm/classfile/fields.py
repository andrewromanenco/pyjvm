"""Class fields."""

from collections import namedtuple
from pyjvm.classfile.access_flags import read_access_flags
from pyjvm.classfile.attributes import read_attributes

Field = namedtuple(
    'Field',
    ['access_flags', 'name_index', 'descriptor_index', 'attributes_count', 'attributes'])

Attribute = namedtuple(
    'Attribute',
    ['attribute_name_index', 'attribute_length', 'info']
    )

def read_fields(reader):
    """Read fields from a reader."""
    fields_count = reader.get_u2()
    fields = []
    while fields_count > 0:
        access_flags = read_access_flags(reader)
        name_index = reader.get_u2()
        descriptor_index = reader.get_u2()
        attributes = read_attributes(reader)
        fields.append(Field(
            access_flags,
            name_index,
            descriptor_index,
            len(attributes),
            attributes
            ))
        fields_count -= 1
    return fields
