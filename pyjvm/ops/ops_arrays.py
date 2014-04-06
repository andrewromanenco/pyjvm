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
'''Java bytecode implementation'''

import logging

from pyjvm.jassert import jassert_array
from pyjvm.jassert import jassert_float
from pyjvm.jassert import jassert_double
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long
from pyjvm.jassert import jassert_ref
from pyjvm.jvmo import JArray

logger = logging.getLogger(__name__)


def op_0x2e(frame):  # iaload
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    frame.stack.append(values[index])


def op_0x2f(frame):  # laload
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    frame.stack.append(values[index])


def op_0x30(frame):  # faload
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    frame.stack.append(values[index])


def op_0x31(frame):  # daload
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    frame.stack.append(values[index])


def op_0x32(frame):  # aaload
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    frame.stack.append(values[index])


def op_0x33(frame):  # baload
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    frame.stack.append(values[index])


def op_0x34(frame):  # caload
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    frame.stack.append(values[index])


def op_0x35(frame):  # saload
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    frame.stack.append(values[index])


def op_0x4f(frame):  # iastore
    value = frame.stack.pop()
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(value)
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    values[index] = value


def op_0x50(frame):  # lastore
    value = frame.stack.pop()
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_long(value)
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    values[index] = value


def op_0x51(frame):  # fastore
    value = frame.stack.pop()
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_float(value)
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    values[index] = value


def op_0x52(frame):  # dastore
    value = frame.stack.pop()
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_double(value)
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    values[index] = value


def op_0x53(frame):  # aastore
    # TODO ArrayStoreException
    value = frame.stack.pop()
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_ref(value)
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    values[index] = value


def op_0x54(frame):  # bastore
    value = frame.stack.pop()
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(value)
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    values[index] = value


def op_0x55(frame):  # castore
    value = frame.stack.pop()
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(value)
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    values[index] = value


def op_0x56(frame):  # sastore
    value = frame.stack.pop()
    index = frame.stack.pop()
    ref = frame.stack.pop()
    jassert_int(value)
    jassert_int(index)
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    values = array.values
    if index < 0 or index >= len(values):
        frame.vm.raise_exception(frame,
                                 "java/lang/ArrayIndexOutOfBoundsException")
        return
    values[index] = value


def op_0xbc(frame):  # newarray (array of primitives)
    atype = ord(frame.code[frame.pc])
    frame.pc += 1
    count = frame.stack.pop()
    jassert_int(count)
    if count < 0:
        frame.vm.raise_exception(frame, "java/lang/NegativeArraySizeException")
        return
    values = None
    if atype in [10, 5, 8, 9, 4]:  # int, char, byte, short, boolean
        values = [0]*count
    elif atype == 7:  # double
        values = [("double", 0.0)] * count
    elif atype == 6:  # float
        values = [("float", 0.0)] * count
    elif atype == 11:  # long
        values = [("long", 0)] * count
    else:
        raise Exception("Array creation for ATYPE {0} not yet supported"
                        .format(atype))
    prims = {4: "[Z", 5: "[C", 6: "[F", 7: "[D", 8: "[B", 9: "[S",
             10: "[I", 11: "[J"}
    array_class = frame.vm.get_class(prims[atype])
    jarray = JArray(array_class, frame.vm)
    jarray.values = values
    ref = frame.vm.add_to_heap(jarray)
    frame.stack.append(ref)


def op_0xbd(frame):  # anewarray (array of refs)
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_item = frame.this_class.constant_pool[index]
    assert cp_item[0] == 7  # CONSTANT_Class
    klass_name = frame.this_class.constant_pool[cp_item[1]][1]
    assert type(klass_name) is unicode
    frame.vm.get_class(klass_name)  # make sure it is loaded

    count = frame.stack.pop()
    jassert_int(count)
    if count < 0:
        frame.vm.raise_exception(frame, "java/lang/NegativeArraySizeException")
        return

    values = [None] * count
    array_class = frame.vm.get_class("[L" + klass_name + ";")
    jarray = JArray(array_class, frame.vm)
    jarray.values = values
    ref = frame.vm.add_to_heap(jarray)
    frame.stack.append(ref)


def op_0xbe(frame):  # arraylength
    ref = frame.stack.pop()
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    assert ref[0] == "ref"
    array = frame.vm.heap[ref[1]]
    jassert_array(array)
    length = len(array.values)
    frame.stack.append(length)


def op_0xc5(frame):  # multianewarray
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    dims = ord(frame.code[frame.pc])
    frame.pc += 1
    if dims < 1:
        frame.vm.raise_exception(frame, "java/lang/NegativeArraySizeException")
        return

    cp_item = frame.this_class.constant_pool[index]
    if cp_item[0] != 7:
        raise Exception("This use case is not yet supported in mdim-array")
    klass_name = frame.this_class.constant_pool[cp_item[1]][1]
    while klass_name[0] == '[':
        klass_name = klass_name[1:]

    counts = []
    for i in range(dims):
        counts.insert(0, frame.stack.pop())

    def mla(counts, klass_name):
        if len(counts) == 1:
            if klass_name in ('B', 'C', 'I', 'S', 'Z'):
                default = 0
            elif klass_name == 'D':
                default = ('double', 0.0)
            elif klass_name == 'F':
                default = ('float', 0.0)
            elif klass_name == 'J':
                default = ('long', 0)
            elif klass_name[0] == 'L':
                default = None
            array_class = frame.vm.get_class('[' + klass_name)
            array = JArray(array_class, frame.vm)
            values = [default] * counts[0]
            array.values = values
            ref = frame.vm.add_to_heap(array)
            return ref
        else:
            name = '[' * len(counts)
            name += klass_name
            array_class = frame.vm.get_class(name)
            array = JArray(array_class, frame.vm)
            values = [None] * counts[0]
            for i in range(counts[0]):
                values[i] = mla(counts[1:], klass_name)
            array.values = values
            ref = frame.vm.add_to_heap(array)
            return ref

    ref = mla(counts, klass_name)
    frame.stack.append(ref)
