"""Access flags related stuff."""

from enum import Enum

class AccessFlag(Enum):
    """Access flag constants."""

    ACC_PUBLIC = 0x0001
    ACC_PRIVATE = 0x0002
    ACC_PROTECTED = 0x0004
    ACC_STATIC = 0x0008
    ACC_FINAL = 0x0010
    ACC_SUPER = 0x0020
    ACC_VOLATILE = 0x0040
    ACC_TRANSIENT = 0x0080
    ACC_INTERFACE = 0x0200
    ACC_ABSTRACT = 0x0400
    ACC_SYNTHETIC = 0x1000
    ACC_ANNOTATION = 0x2000
    ACC_ENUM = 0x4000


def read_access_flags(reader):
    """Read access flags and return them as FlagSet."""
    flag_bits = reader.get_u2()
    builder = FlagSetBuilder()
    for flag in AccessFlag:
        if flag_bits & flag.value:
            builder.set(flag)
    return builder.build()

class FlagSetBuilder:
    """Builder for immutable flags set."""

    def __init__(self):
        """Creates new builder."""
        self.flags = {}

    def set(self, access_flag):
        """Adds a flag to set."""
        self.flags[access_flag] = 1
        return self

    def build(self):
        """Builds a flag set."""
        return FlagSet(self.flags)

class FlagSet:
    """Set of flags."""

    def __init__(self, flags_dictionary):
        """Init set with given dictionary."""
        self.flags = flags_dictionary

    def is_set(self, flag):
        """Checks if a flag is set."""
        return flag in self.flags

    def __str__(self):
        return str(list(self.flags.keys()))
