"""In memory representation of parsed bytecode."""

class JavaClassBuilder:
    """Util to build immutable java class."""

    def __init__(self):
        """Init new builder."""
        self.constant_pool = None
        self.access_flags = None
        self.this_index = -1
        self.super_index = -1
        self.interface_indexes = None

    def with_constant_pool(self, cpool):
        """Assign constant pool."""
        self.constant_pool = cpool
        return self

    def with_access_flags(self, access_flags):
        """Assign class access flags."""
        self.access_flags = access_flags
        return self

    def with_this_class_index(self, index):
        """Set index of the class ref in constant pool."""
        self.this_index = index
        return self

    def with_super_class_index(self, index):
        """Set index of super class ref in constant pool."""
        self.super_index = index
        return self

    def with_interface_indexes(self, interface_indexes):
        """Set indexes of class interfaces from constant pool."""
        self.interface_indexes = interface_indexes
        return self

    def build(self):
        """Build java class representation."""
        return JavaClass(self)


class JavaClass:
    """Java class immutable representation."""

    def __init__(self, java_class_builder):
        """Init a java class."""
        if java_class_builder.constant_pool is None:
            raise Exception("Constant pool is not provided")
        if java_class_builder.access_flags is None:
            raise Exception("Access flags are not provided")
        if java_class_builder.interface_indexes is None:
            raise Exception("Interface indexes were not set")
        self.constant_pool = java_class_builder.constant_pool
        self.access_flags = java_class_builder.access_flags
        self.this_index = java_class_builder.this_index
        self.super_index = java_class_builder.super_index
        self.interface_indexes = java_class_builder.interface_indexes
