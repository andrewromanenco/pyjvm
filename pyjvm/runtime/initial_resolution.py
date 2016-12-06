def prepare_class(runtime_class):
    static_fields_defs = runtime_class.get_static_fields_definitions()
    for field in static_fields_defs:
        runtime_class.set_field(field.name, default_for_type(field.type))


def default_for_type(type_name):
    '''Default values for primiteves and refs'''
    if type_name == "I":
        return 0
    elif type_name == "J":  # long
        return 0
    elif type_name == "[":  # array
        return None
    elif type_name == 'L':  # object
        return None
    elif type_name == 'Z':  # boolean
        return 0
    elif type_name == 'D':  # double
        return 0.0
    elif type_name == 'F':  # float
        return 0.0
    elif type_name == 'C':  # float
        return 0
    elif type_name == 'B':  # byte
        return 0
    elif type_name == 'S':  # short
        return 0
    raise Exception("Default value not supported for " + str(type_name))


'''

Field = namedtuple('Field', [
    'access_flags', 'name_index', 'descriptor_index', 'attributes_count',
    'attributes'
])

'''
