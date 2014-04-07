BYTECODE = {}


def bytecode(code):
    def cl(func):
        BYTECODE[hex(code)] = func
        return func

    return cl


def get_operation(code):
    return BYTECODE.get(code)