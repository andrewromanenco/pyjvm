# PyJVM (pyjvm.org) Java Virtual Machine implemented in pure Python
# Copyright (C) 2014 Andrew Romanenco (andrew@romanenco.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''Class loader. Binary to python representation'''

import logging
import os
import struct
from pyjvm import jarfile

from pyjvm.jvmo import JavaClass

logger = logging.getLogger(__name__)


def class_loader(class_name, (lookup_paths, jars, rt)):
    '''Get JavaClass from class file.
    Order of lookup: rt.jar, other jars from class path, folders
    from class path
    '''
    logger.debug("Loading class {0}".format(class_name))
    assert class_name[0] != '['  # no arrays
    file_path = class_name + ".class"
    f = None
    jar_file = None
    if file_path in rt:
        path = rt[file_path]
        jar_file = jarfile.jar(path)
        f = jar_file.open(file_path)
        logger.debug("Loading %s from %s", file_path, path)
    elif file_path in jars:
        path = jars[file_path]
        jar_file = jarfile.jar(path)
        f = jar_file.open(file_path)
        logger.debug("Loading %s from %s", file_path, path)
    else:
        for directory in lookup_paths:
            path = os.path.join(directory, file_path)
            if os.path.exists(path) and not os.path.isdir(path):
                f = open(path, "rb")
                break
            logger.debug("Loading from file %s", path)
    if f is None:
        raise Exception("Class not found " + class_name)

    # file discovered, read step by step
    try:
        cafebabe(f)
        jdk7(f)
        constant_pool = read_constant_pool(f)
        class_flags = access_flags(f)
        (this_name, super_name) = this_super(f)
        all_interfaces = interfaces(f)
        all_fields = fields(f)
        all_methods = methods(f)
    except Exception:
        raise
    finally:
        f.close()
    return make_class(this_name, super_name, constant_pool, all_fields,
                      all_methods, all_interfaces, class_flags)


# EXACTLY THE SAME RESULTS COME FROM PYTHON's struct MODULE
# Here both approaches are used to make real reading process cleaner

def getU1(f):
    '''Single byte'''
    byte1 = f.read(1)
    return ord(byte1)


def getU2(f):
    '''Two bytes'''
    byte1 = f.read(1)
    byte2 = f.read(1)
    return (ord(byte1) << 8) + ord(byte2)


def getU4(f):
    '''4 bytes'''
    byte1 = f.read(1)
    byte2 = f.read(1)
    byte3 = f.read(1)
    byte4 = f.read(1)
    return (ord(byte1) << 24) + (ord(byte2) << 16) + (ord(byte3) << 8) \
        + ord(byte4)


def getUV(f, length):
    '''variable length'''
    data = f.read(length)
    return data


def cafebabe(f):
    '''Make sure this is java'''
    cb = [0xCA, 0xFE, 0xBA, 0xBE]
    index = 0
    while index < 4:
        byte = getU1(f)
        if byte != cb[index]:
            raise Exception("No CAFEBABE")
        index += 1


def jdk7(f):
    '''Make sure this is java 7 class'''
    getU2(f)
    major = getU2(f)
    if major != 0x33:  # 52 - jdk7
        raise Exception("Not a jdk7 class")


def read_constant_pool(f):
    '''Constant pools starts with index 1'''
    pool = ["ZERO"]
    cp_size = getU2(f)
    count = 1
    while count < cp_size:
        cp_type = getU1(f)
        if cp_type == 10:  # CONSTANT_Methodref
            pool.append([10, getU2(f), getU2(f)])
        elif cp_type == 11:  # CONSTANT_InterfaceMethodref
            pool.append([11, getU2(f), getU2(f)])
        elif cp_type == 9:  # CONSTANT_Fieldref
            pool.append([9, getU2(f), getU2(f)])
        elif cp_type == 8:  # CONSTANT_String
            pool.append([8, getU2(f)])
        elif cp_type == 7:  # CONSTANT_Class
            pool.append([7, getU2(f)])
        elif cp_type == 6:  # CONSTANT_Double
            value = struct.unpack('>d', f.read(8))[0]
            pool.append([6, value])
            count += 1  # double space in cp
            pool.append("EMPTY_SPOT")
        elif cp_type == 1:  # CONSTANT_Utf8
            length = getU2(f)
            data = getUV(f, length)
            value = unicode("")
            index = 0
            while index < length:
                c = struct.unpack(">B", data[index])[0]
                if (c >> 7) == 0:
                    value += unichr(c)
                    index += 1
                elif (c >> 5) == 0b110:
                    b = ord(data[index + 1])
                    assert b & 0x80
                    c = ((c & 0x1f) << 6) + (b & 0x3f)
                    value += unichr(c)
                    index += 2
                elif (c >> 4) == 0b1110:
                    y = ord(data[index + 1])
                    z = ord(data[index + 2])
                    c = ((c & 0xf) << 12) + ((y & 0x3f) << 6) + (z & 0x3f)
                    value += unichr(c)
                    index += 3
                elif c == 0b11101101:
                    v = ord(data[index + 1])
                    w = ord(data[index + 2])
                    # x = ord(data[index + 3]) No need this is marker
                    y = ord(data[index + 4])
                    z = ord(data[index + 5])
                    c = 0x10000 + ((v & 0x0f) << 16) + ((w & 0x3f) << 10) \
                        + ((y & 0x0f) << 6) + (z & 0x3f)
                    value += unichr(c)
                    index += 6
                else:
                    raise Exception("UTF8 is not fully implemented {0:b}"
                                    .format(c))
            pool.append([1, value])
        elif cp_type == 4:  # CONSTANT_Float
            value = struct.unpack('>f', f.read(4))[0]
            pool.append([4, value])
        elif cp_type == 12:  # CONSTANT_NameAndType
            pool.append([12, getU2(f), getU2(f)])
        elif cp_type == 3:  # CONSTANT_Int
            data = f.read(4)
            value = struct.unpack('>i', data)[0]
            # pool.append([3, getU4(f)])
            pool.append([3, value])
        elif cp_type == 5:  # CONSTANT_Long
            value = struct.unpack('>q', f.read(8))[0]
            pool.append([5, value])
            count += 1  # double space in cp
            pool.append("EMPTY_SPOT")
        else:
            raise Exception("Not implemented constant pool entry tag: %s",
                            str(cp_type))
        count += 1
    return pool


def access_flags(f):
    '''Read flags'''
    flags = getU2(f)
    return flags


def this_super(f):
    '''Constant pool indexes for this/super names.
    Resolve later to unicode/class
    '''
    this_name = getU2(f)
    super_class = getU2(f)
    return (this_name, super_class)


def interfaces(f):
    '''Not really used at runtime, other than casts'''
    data = []
    int_count = getU2(f)
    for i in range(int_count):
        index = getU2(f)
        data.append(index)
    return data


def fields(f):
    '''Read all fields from .class'''
    fields_count = getU2(f)
    data = []
    for i in range(fields_count):
        flags = access_flags(f)
        name = getU2(f)
        desc = getU2(f)
        attributes_count = getU2(f)
        attrs = []
        for k in range(attributes_count):
            attr_name = getU2(f)
            attr_len = getU4(f)
            attr_data = getUV(f, attr_len)
            attrs.append((attr_name, attr_data))
        # flags, name and description, attrs
        data.append((flags, name, desc, attrs))
    return data


def methods(f):
    '''Read all methods from .class'''
    methods_count = getU2(f)
    data = []
    for i in range(methods_count):
        flag = getU2(f)
        name = getU2(f)
        desc = getU2(f)
        attr_count = getU2(f)
        attrs = []
        for k in range(attr_count):
            attr_name = getU2(f)
            attr_len = getU4(f)
            attr_data = getUV(f, attr_len)
            attrs.append((attr_name, attr_data))
        data.append((flag, name, desc, attrs))
    return data


def make_class(this_name, super_name, constant_pool, all_fields, all_methods,
               all_interfaces, class_flags):
    '''Actually construct java class from data read earlier'''
    jc = JavaClass()
    jc.flags = class_flags
    if class_flags & 0x0200:  # is interface
        jc.is_interface = True
    jc.constant_pool = constant_pool
    jc.this_name = resolve_to_string(constant_pool, this_name)
    if super_name != 0:
        jc.super_class = resolve_to_string(constant_pool, super_name)
    add_fields(jc, constant_pool, all_fields)
    add_methods(jc, constant_pool, all_methods)
    add_interfaces(jc, constant_pool, all_interfaces)
    return jc


def resolve_to_string(constant_pool, index):
    '''Unicode string for constant pool entry'''
    data = constant_pool[index]
    if data[0] == 1:
        return unicode(data[1])
    elif data[0] == 7:
        return resolve_to_string(constant_pool, data[1])
    elif data[0] == 12:
        return resolve_to_string(constant_pool, data[1])
    else:
        raise Exception("Not supported string resolution step: {0}".
                        format(data[0]))


def add_fields(jc, constant_pool, data):  # list of (flag, name, desc)
    '''Both static and instance fields'''
    for field in data:
        static = True if field[0] & 0x0008 > 0 else False
        name = resolve_to_string(constant_pool, field[1])
        desc = resolve_to_string(constant_pool, field[2])
        if static:
            default_value = default_for_type(desc)
            jc.static_fields[name] = [desc, default_value]
        else:
            jc.member_fields[name] = desc


def default_for_type(desc):
    '''Default values for primiteves and refs'''
    if desc == "I":
        return 0
    elif desc == "J":  # long
        return ("long", 0)
    elif desc[0] == "[":  # array
        return None
    elif desc[0] == 'L':  # object
        return None
    elif desc == 'Z':  # boolean
        return 0
    elif desc == 'D':  # double
        return ('double', 0.0)
    elif desc == 'F':  # float
        return ('float', 0.0)
    elif desc == 'C':  # float
        return 0
    elif desc == 'B':  # byte
        return 0
    elif desc == 'S':  # short
        return 0
    raise Exception("Default value not yet supported for " + str(desc))


def parse_code(code, constant_pool):
    '''Each non abstract/native method has this struc'''
    nargs = (ord(code[2]) << 8) + ord(code[3])
    code_len = (ord(code[4]) << 24) + (ord(code[5]) << 16) + \
        (ord(code[6]) << 8) + ord(code[7])
    ex_len = (ord(code[8 + code_len]) << 8) + ord(code[8 + code_len + 1])
    ex_base = 8 + code_len + 2
    extable = []
    for i in range(ex_len):
        data = code[ex_base + i*8:ex_base + i*8 + 8]
        start_pc = struct.unpack('>H', data[0:2])[0]
        end_pc = struct.unpack('>H', data[2:4])[0]
        handler_pc = struct.unpack('>H', data[4:6])[0]
        catch_type = struct.unpack('>H', data[6:8])[0]
        type_name = None
        if catch_type > 0:
            cp_item = constant_pool[catch_type]
            assert cp_item[0] == 7
            type_name = constant_pool[cp_item[1]][1]
        e = (start_pc, end_pc, handler_pc, catch_type, type_name)
        extable.append(e)
    return (code[8:8+code_len], nargs, extable)


def parse_exceptions(data, constant_pool):
    '''See jvm 7 spec for details'''
    count = (ord(data[0]) << 8) + ord(data[1])
    exceptions = []
    for i in range(count):
        index = struct.unpack('>H', data[i*2 + 2:i*2+4])[0]
        cp_item = constant_pool[index]
        assert cp_item[0] == 7
        ex = constant_pool[cp_item[1]][1]
        exceptions.append(ex)
    return exceptions


def add_methods(jc, constant_pool, data):
    '''Add methods information'''
    # data is a list list of flag, name, desc, attrs; attr list of name/data
    for method in data:
        flags = method[0]
        name = resolve_to_string(constant_pool, method[1])
        desc = resolve_to_string(constant_pool, method[2])
        code = None
        exceptions = []
        for attr in method[3]:
            attr_name = resolve_to_string(constant_pool, attr[0])
            if attr_name == "Code":
                code = attr[1]
            elif attr_name == "Exceptions":
                exception = parse_exceptions(attr[1], constant_pool)
                # ignore
            elif attr_name in ("Signature", "Deprecated",
                               "RuntimeVisibleAnnotations"):
                pass
            else:
                raise Exception("Unsupported attr {0} in {1}".format(attr_name,
                                name))
        if code is None and (flags & (0x0100 + 0x0400)) == 0:
            raise Exception("No code attr in {0}".format(name))
        if name not in jc.methods:
            jc.methods[name] = {}
        m = jc.methods[name]
        if code is not None:
            code = parse_code(code, constant_pool)
        else:
            code = ("<NATIVE>", 0, [])
        m[desc] = (flags, code[1], code[0], code[2], exceptions)


def add_interfaces(jc, constant_pool, all_interfaces):
    for i in all_interfaces:
        name = resolve_to_string(constant_pool, i)
        jc.interfaces.append(name)
