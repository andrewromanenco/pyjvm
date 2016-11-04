"""Class fields."""

from collections import namedtuple

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
        access_flags = reader.get_u2()
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

def read_attributes(reader):
    """Read attributes from a stream."""
    attr_count = reader.get_u2()
    attributes = []
    while attr_count > 0:
        attribute_name_index = reader.get_u2()
        attribute_length = reader.get_u2()
        info = reader.get_uv(attribute_length)
        attributes.append(Attribute(
            attribute_name_index,
            attribute_length,
            info
            ))
        attr_count -= 1
    return attributes
