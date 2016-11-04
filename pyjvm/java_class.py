"""In memory representation of parsed bytecode."""

class JavaClassBuilder:
    """Util to build immutable java class."""

    def __init__(self):
        """Init new builder."""
        self.constant_pool = None
        self.access_flags = None
        self.this_index = -1
        self.super_index = -1

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

    def build(self):
        """Build java class representation."""
        if self.constant_pool is None:
            raise Exception("Constant pool is not provided")
        if self.access_flags is None:
            raise Exception("Access flags are not provided")
        return JavaClass(
            self.constant_pool,
            self.access_flags,
            self.this_index,
            self.super_index)


class JavaClass:
    """Java class immutable representation."""

    def __init__(self, constant_pool, access_flags, this_index, super_index):
        """Init a java class."""
        self.constant_pool = constant_pool
        self.access_flags = access_flags
        self.this_index = this_index
        self.super_index = super_index
