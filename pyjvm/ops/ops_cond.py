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

from pyjvm.bytecode import bytecode
from pyjvm.checkcast import checkcast
from pyjvm.jassert import jassert_float
from pyjvm.jassert import jassert_double
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long
from pyjvm.jassert import jassert_ref
from pyjvm.jvmo import JavaObject
from pyjvm.vmo import vmo_check_cast, VM_CLASS_NAMES


@bytecode(code=0x94)
def lcmpl(frame):
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


@bytecode(code=0x95)
def fcmpl(frame):
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


@bytecode(code=0x96)
def fcmpg(frame):
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


@bytecode(code=0x97)
def dcmpl(frame):
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


@bytecode(code=0x98)
def dcmpl(frame):
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


@bytecode(code=0x99)
def if_eq(frame):
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value == 0:
        frame.pc += offset - 2 - 1


@bytecode(code=0x9a)
def ifne(frame):
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value != 0:
        frame.pc += offset - 2 - 1


@bytecode(code=0x9b)
def iflt(frame):
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value < 0:
        frame.pc += offset - 2 - 1


@bytecode(code=0x9c)
def ifge(frame):
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value >= 0:
        frame.pc += offset - 2 - 1


@bytecode(code=0x9d)
def ifgt(frame):
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value > 0:
        frame.pc += offset - 2 - 1


@bytecode(code=0x9e)
def ifle(frame):
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_int(value)
    if value <= 0:
        frame.pc += offset - 2 - 1


@bytecode(code=0x9f)
def if_icmpeq(frame):
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


@bytecode(code=0xa0)
def if_icmpne(frame):
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


@bytecode(code=0xa1)
def if_icmplt(frame):
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


@bytecode(code=0xa2)
def if_icmpge(frame):
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


@bytecode(code=0xa3)
def if_icmpgt(frame):
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


@bytecode(code=0xa4)
def if_icmple(frame):
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


@bytecode(code=0xa5)
def if_acmpeq(frame):
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


@bytecode(code=0xa6)
def if_acmpne(frame):
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


@bytecode(code=0xa7)
def goto(frame):
    data = frame.code[frame.pc:frame.pc + 2]
    frame.pc += 2
    offset = struct.unpack(">h", data)[0]
    frame.pc += offset - 2 - 1


@bytecode(code=0xa8)
def jsr(frame):
    frame.stack.append(frame.pc + 2)
    data = frame.code[frame.pc:frame.pc + 2]
    frame.pc += 2
    offset = struct.unpack(">h", data)[0]
    frame.pc += offset - 2 - 1


@bytecode(code=0xaa)
def tableswitch(frame):
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


@bytecode(code=0xab)
def lookupswitch(frame):
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


@bytecode(code=0xc6)
def ifnull(frame):
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_ref(value)
    if value is None:
        frame.pc += offset - 2 - 1


@bytecode(code=0xc7)
def ifnonnull(frame):
    byte1 = ord(frame.code[frame.pc])
    byte2 = ord(frame.code[frame.pc + 1])
    frame.pc += 2
    offset = struct.unpack(">h", chr(byte1) + chr(byte2))[0]
    value = frame.stack.pop()
    jassert_ref(value)
    if value is not None:
        frame.pc += offset - 2 - 1


@bytecode(code=0xc0)
def checkcast_(frame):   # FIXME: rename pyjvm.checkcast and rename this func to checkcast 
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


@bytecode(code=0xc1)
def instanceof(frame):
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


@bytecode(code=0xc8)
def goto_w(frame):
    data = frame.code[frame.pc:frame.pc + 4]
    frame.pc += 4
    offset = struct.unpack(">i", data)[0]
    frame.pc += offset - 4 - 1


@bytecode(code=0xc9)
def jsr_w(frame):
    frame.stack.append(frame.pc + 4)
    data = frame.code[frame.pc:frame.pc + 4]
    frame.pc += 4
    offset = struct.unpack(">i", data)[0]
    frame.pc += offset - 4 - 1
