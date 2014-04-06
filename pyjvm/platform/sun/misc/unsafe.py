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
'''See natives.txt in documentation'''

import struct

from pyjvm.utils import str_to_string


def sun_misc_Unsafe_arrayBaseOffset__Ljava_lang_Class__I(frame, args):
    frame.stack.append(0)


def sun_misc_Unsafe_arrayIndexScale__Ljava_lang_Class__I(frame, args):
    frame.stack.append(1)


def sun_misc_Unsafe_addressSize___I(frame, args):
    frame.stack.append(4)


def java_util_concurrent_atomic_AtomicLong_VMSupportsCS8___Z(frame, args):
    frame.stack.append(1)


def sun_misc_Unsafe_objectFieldOffset__Ljava_lang_reflect_Field__J(frame, args):
    ref = args[1]
    assert type(ref) is tuple and ref[0] == "ref"
    field = frame.vm.heap[ref[1]]
    name = str_to_string(frame.vm, field.fields["name"])
    k_ref = field.fields["clazz"]
    klass_object = frame.vm.heap[k_ref[1]]
    klass = frame.vm.get_class(klass_object.fields["@CLASS_NAME"])
    o = klass.get_instance(frame.vm)
    index = 0
    for key in o.fields:
        if key == name:
            frame.stack.append(("long", index))
            return
        index += 1
    assert False  # should never get here


def sun_misc_Unsafe_compareAndSwapLong__Ljava_lang_Object_JJJ_Z(frame, args):
    ref = args[1]
    offset = args[2]
    expected = args[4]
    x = args[6]
    assert type(ref) is tuple and ref[0] == "ref"
    assert type(offset) is tuple and offset[0] == "long"
    assert type(expected) is tuple and expected[0] == "long"
    assert type(x) is tuple and x[0] == "long"
    o = frame.vm.heap[ref[1]]
    index = 0
    name = None
    for field in o.fields:
        if index == offset[1]:
            name = field
        index += 1
    assert name is not None
    if o.fields[name] == expected:
        o.fields[name] = x
        frame.stack.append(1)
    else:
        frame.stack.append(0)


def sun_misc_Unsafe_compareAndSwapInt__Ljava_lang_Object_JII_Z(frame, args):
    ref = args[1]
    offset = args[2]
    expected = args[4]
    x = args[5]
    assert type(ref) is tuple and ref[0] == "ref"
    assert type(offset) is tuple and offset[0] == "long"
    assert type(expected) is int
    assert type(x) is int
    o = frame.vm.heap[ref[1]]
    index = 0
    name = None
    for field in o.fields:
        if index == offset[1]:
            name = field
        index += 1
    assert name is not None
    if o.fields[name] == expected:
        o.fields[name] = x
        frame.stack.append(1)
    else:
        frame.stack.append(0)


memory = {}


def sun_misc_Unsafe_allocateMemory__J_J(frame, args):
    global memory
    l = args[1]
    assert type(l) is tuple and l[0] == "long"
    chunk = [0]*l[1]
    index = 1  # bad
    while index in memory:
        index += 1
    memory[index] = chunk
    frame.stack.append(("long", index))


def sun_misc_Unsafe_putLong__JJ_V(frame, args):
    global memory
    address = args[1]
    value = args[3]
    assert type(address) is tuple and address[0] == "long"
    assert type(value) is tuple and value[0] == "long"
    chunk = memory[address[1]]
    bytes = struct.pack(">q", value[1])
    chunk[0:8] = bytes[0:8]


def sun_misc_Unsafe_getByte__J_B(frame, args):
    global memory
    address = args[1]
    assert type(address) is tuple and address[0] == "long"
    chunk = memory[address[1]]
    b = struct.unpack(">b", chunk[0])[0]
    frame.stack.append(b)


def sun_misc_Unsafe_freeMemory__J_V(frame, args):
    global memory
    address = args[1]
    assert type(address) is tuple and address[0] == "long"
    del memory[address[1]]


def sun_misc_Unsafe_putOrderedObject__Ljava_lang_Object_JLjava_lang_Object__V(frame, args):
    ref_o = args[1]
    index = args[2][1]  # from long
    ref_x = args[4]
    o = frame.vm.heap[ref_o[1]]
    if o.java_class.is_array:
        o.values[index] = ref_x
    else:
        for field in o.fields:
            if index == 0:
                name = field
            index -= 1
        assert name is not None
        o.fields[name] = ref_x


def sun_misc_Unsafe_getObject__Ljava_lang_Object_J_Ljava_lang_Object_(frame, args):
    ref_o = args[1]
    index = args[2][1]  # from long
    o = frame.vm.heap[ref_o[1]]
    assert o.java_class.is_array
    frame.stack.append(o.values[index])


def sun_misc_Unsafe_getObjectVolatile__Ljava_lang_Object_J_Ljava_lang_Object_(frame, args):
    ref_o = args[1]
    index = args[2][1]  # from long
    o = frame.vm.heap[ref_o[1]]
    assert o.java_class.is_array
    frame.stack.append(o.values[index])


def sun_misc_Unsafe_compareAndSwapObject__Ljava_lang_Object_JLjava_lang_Object_Ljava_lang_Object__Z(frame, args):
    ref_o = args[1]
    offset = args[2][1]  # long value
    ref_expected = args[4]
    ref_x = args[5]
    o = frame.vm.heap[ref_o[1]]
    assert o.java_class.is_array
    if o.values[offset] == ref_expected:
        o.values[offset] = ref_x
        frame.stack.append(1)
    else:
        frame.stack.append(0)
