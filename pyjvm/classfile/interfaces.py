"""Interfaces related code."""

def read_interfaces(reader):
    """Read interfaces for the class."""
    count = reader.get_u2()
    interface_indexes = []
    while count > 0:
        interface_indexes.append(reader.get_u2())
        count -= 1
    return interface_indexes
