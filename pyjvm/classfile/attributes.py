"""Field and method attributes."""

from collections import namedtuple

Attribute = namedtuple('Attribute',
                       ['attribute_name_index', 'attribute_length', 'info'])


def read_attributes(reader):
    """Read attributes from a stream."""
    attr_count = reader.get_u2()
    attributes = []
    while attr_count > 0:
        attribute_name_index = reader.get_u2()
        attribute_length = reader.get_u4()
        info = reader.get_uv(attribute_length)
        attributes.append(
            Attribute(attribute_name_index, attribute_length, info))
        attr_count -= 1
    return attributes
