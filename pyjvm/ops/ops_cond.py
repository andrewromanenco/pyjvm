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

import struct

from pyjvm.checkcast import checkcast
from pyjvm.jassert import jassert_float
from pyjvm.jassert import jassert_double
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long
from pyjvm.jassert import jassert_ref
from pyjvm.jvmo import JavaObject
from pyjvm.vmo import vmo_check_cast, VM_CLASS_NAMES


def op_0x94(frame):  # lcmpl
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_long(value1)
    jassert_long(value2)
    if value1[1] > value2[1]:
        frame.stack.append(1)
    elif value1[1] == value2[1]:
        frame.stack.append(0)
    else:
        frame.stack.append(-1)


def op_0x95(frame):  # fcmpl
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    if value1[1] > value2[1]:
        frame.stack.append(1)
    elif value1 == value2:
        frame.stack.append(0)
    else:
        frame.stack.append(-1)


def op_0x96(frame):  # fcmpg
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    if value1[1] > value2[1]:
        frame.stack.append(1)
    elif value1 == value2:
        frame.stack.append(0)
    else:
        frame.stack.append(-1)


def op_0x97(frame):  # dcmpl
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    if value1[1] > value2[1]:
        frame.stack.append(1)
    elif value1 == value2:
        frame.stack.append(0)
    else:
        frame.stack.append(-1)


def op_0x98(frame):  # dcmpl
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    if value1[1] > value2[1]:
        frame.stack.append(1)
    elif value1 == value2:
        frame.stack.append(0)
    else:
        frame.stack.append(-1)


def op_0x99(frame):  # if_eq
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value == 0:
        frame.pc += offset - 2 - 1


def op_0x9a(frame):  # ifne
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value != 0:
        frame.pc += offset - 2 - 1


def op_0x9b(frame):  # iflt
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value < 0:
        frame.pc += offset - 2 - 1


def op_0x9c(frame):  # ifge
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value >= 0:
        frame.pc += offset - 2 - 1


def op_0x9d(frame):  # ifgt
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value > 0:
        frame.pc += offset - 2 - 1


def op_0x9e(frame):  # ifle
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value <= 0:
        frame.pc += offset - 2 - 1


def op_0x9f(frame):  # if_icmpeq
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value1)
    jassert_int(value2)
    if value1 == value2:
        frame.pc += offset - 2 - 1


def op_0xa0(frame):  # if_icmpne
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value1)
    jassert_int(value2)
    if value1 != value2:
        frame.pc += offset - 2 - 1


def op_0xa1(frame):  # if_icmplt
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value1)
    jassert_int(value2)
    if value1 < value2:
        frame.pc += offset - 2 - 1


def op_0xa2(frame):  # if_icmpge
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value1)
    jassert_int(value2)
    if value1 >= value2:
        frame.pc += offset - 2 - 1


def op_0xa3(frame):  # if_icmpgt
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value1)
    jassert_int(value2)
    if value1 > value2:
        frame.pc += offset - 2 - 1


def op_0xa4(frame):  # if_icmple
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value1)
    jassert_int(value2)
    if value1 <= value2:
        frame.pc += offset - 2 - 1


def op_0xa5(frame):  # if_acmpeq
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_ref(value1)
    jassert_ref(value2)
    if value1 == value2:
        frame.pc += offset - 2 - 1


def op_0xa6(frame):  # if_acmpne
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_ref(value1)
    jassert_ref(value2)
    if value1 != value2:
        frame.pc += offset - 2 - 1


def op_0xa7(frame):  # goto
    data = frame.code[frame.pc:frame.pc + 2]
    frame.pc += 2
    offset = struct.unpack(">h", data)[0]
    frame.pc += offset - 2 - 1


def op_0xa8(frame):  # jsr
    frame.stack.append(frame.pc + 2)
    data = frame.code[frame.pc:frame.pc + 2]
    frame.pc += 2
    offset = struct.unpack(">h", data)[0]
    frame.pc += offset - 2 - 1


def op_0xaa(frame):  # tableswitch
    index = frame.stack.pop()
    jassert_int(index)
    last_pc = frame.pc - 1
    while frame.pc % 4 != 0:
        frame.pc += 1
    default = struct.unpack(">i", frame.code[frame.pc:frame.pc + 4])[0]
    frame.pc += 4
    low = struct.unpack(">i", frame.code[frame.pc:frame.pc + 4])[0]
    frame.pc += 4
    high = struct.unpack(">i", frame.code[frame.pc:frame.pc + 4])[0]
    frame.pc += 4
    if index < low or index > high:
        frame.pc = last_pc + default
        return
    count = high - low + 1
    offsets = []
    for i in range(count):
        offsets.append(struct.unpack(">i",
                                     frame.code[frame.pc:frame.pc + 4])[0])
        frame.pc += 4
    frame.pc = last_pc + offsets[index - low]


def op_0xab(frame):  # lookupswitch
    key = frame.stack.pop()
    last_pc = frame.pc - 1
    while frame.pc % 4 != 0:
        frame.pc += 1
    default = struct.unpack(">i", frame.code[frame.pc:frame.pc + 4])[0]
    frame.pc += 4
    npairs = struct.unpack(">i", frame.code[frame.pc:frame.pc + 4])[0]
    frame.pc += 4
    matches = []
    offsets = []
    for i in range(npairs):
        matches.append(struct.unpack(">i",
                                     frame.code[frame.pc:frame.pc + 4])[0])
        frame.pc += 4
        offsets.append(struct.unpack(">i",
                                     frame.code[frame.pc:frame.pc + 4])[0])
        frame.pc += 4
    for i in range(len(matches)):
        if matches[i] == key:
            frame.pc = last_pc + offsets[i]
            return
    frame.pc = last_pc + default


def op_0xc6(frame):  # ifnull
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_ref(value)
    if value is None:
        frame.pc += offset - 2 - 1


def op_0xc7(frame):  # ifnonnull
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_ref(value)
    if value is not None:
        frame.pc += offset - 2 - 1


def op_0xc0(frame):  # checkcast
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    ref = frame.stack.pop()
    if ref is None:
        frame.stack.append(ref)
        return
    cp_item = frame.this_class.constant_pool[index]
    assert cp_item[0] == 7  # CONSTANT_Class_info
    klass_name = frame.this_class.constant_pool[cp_item[1]][1]
    klass = frame.vm.get_class(klass_name)
    object_klass = None
    if ref[1] > 0:  # regular ref
        o = frame.vm.heap[ref[1]]
        object_klass = o.java_class
    else:  # vmo
        object_klass = frame.vm.get_class(VM_CLASS_NAMES[ref[1]])

    if checkcast(object_klass, klass, frame.vm):
        frame.stack.append(ref)
    else:
        frame.vm.raise_exception(frame, "java/lang/ClassCastException")


def op_0xc1(frame):  # instanceof
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    ref = frame.stack.pop()
    if ref is None:
        frame.stack.append(0)
        return
    cp_item = frame.this_class.constant_pool[index]
    assert cp_item[0] == 7  # CONSTANT_Class_info
    klass_name = frame.this_class.constant_pool[cp_item[1]][1]
    klass = frame.vm.get_class(klass_name)
    o = frame.vm.heap[ref[1]]
    object_klass = None
    if ref[1] > 0:  # regular ref
        o = frame.vm.heap[ref[1]]
        object_klass = o.java_class
    else:  # vmo
        object_klass = frame.vm.get_class(VM_CLASS_NAMES[ref[1]])

    if checkcast(object_klass, klass, frame.vm):
        frame.stack.append(1)
    else:
        frame.stack.append(0)


def op_0xc8(frame):  # goto_w
    data = frame.code[frame.pc:frame.pc + 4]
    frame.pc += 4
    offset = struct.unpack(">i", data)[0]
    frame.pc += offset - 4 - 1


def op_0xc9(frame):  # jsr_w
    frame.stack.append(frame.pc + 4)
    data = frame.code[frame.pc:frame.pc + 4]
    frame.pc += 4
    offset = struct.unpack(">i", data)[0]
    frame.pc += offset - 4 - 1
