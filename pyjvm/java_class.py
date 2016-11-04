"""In memory representation of parsed bytecode."""

class JavaClassBuilder:
    """Util to build immutable java class."""

    def __init__(self):
        """Init new builder."""
        self.constant_pool = None

    def with_constant_pool(self, cpool):
        """Assign constant pool."""
        self.constant_pool = cpool
        return self

    def build(self):
        """Build java class representation."""
        if self.constant_pool is None:
            raise Exception("Constant pool is not provided")
        return JavaClass(self.constant_pool)


class JavaClass:
    """Java class immutable representation."""

    def __init__(self, constant_pool):
        """Init a java class."""
        self.constant_pool = constant_pool
