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
from pyjvm.jassert import jassert_ref
from pyjvm.thread import SkipThreadCycle
from pyjvm.utils import category_type


@bytecode(code=0x57)
def pop(frame):
    value = frame.stack.pop()
    assert category_type(value) == 1


@bytecode(code=0x58)
def pop2(frame):
    value = frame.stack.pop()
    if category_type(value) == 2:
        pass
    else:
        value = frame.stack.pop()
        assert category_type(value) == 1


@bytecode(code=0x59)
def dup(frame):
    value = frame.stack.pop()
    assert category_type(value) == 1
    frame.stack.append(value)
    frame.stack.append(value)


@bytecode(code=0x5a)
def dup_x1(frame):
    value1 = frame.stack.pop()
    value2 = frame.stack.pop()
    assert category_type(value1) == 1
    assert category_type(value2) == 1
    frame.stack.append(value1)
    frame.stack.append(value2)
    frame.stack.append(value1)


@bytecode(code=0x5b)
def dup_x2(frame):
    value1 = frame.stack.pop()
    value2 = frame.stack.pop()
    if category_type(value1) == 1 and category_type(value2) == 2:
        # form2
        frame.stack.append(value1)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    value3 = frame.stack.pop()
    if (category_type(value1) == 1 and category_type(value2) == 1 and
            category_type(value3 == 1)):
        # form 1
        frame.stack.append(value1)
        frame.stack.append(value3)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    assert False  # should never get here


@bytecode(code=0x5c)
def dup2(frame):
    value1 = frame.stack.pop()
    if category_type(value1) == 2:
        # form 2
        frame.stack.append(value1)
        frame.stack.append(value1)
        return
    value2 = frame.stack.pop()
    if category_type(value1) == 1 and category_type(value2) == 1:
        # form 1
        frame.stack.append(value2)
        frame.stack.append(value1)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    assert False  # should never get here


@bytecode(code=0x5d)
def dup2_x1(frame):
    value1 = frame.stack.pop()
    value2 = frame.stack.pop()
    if category_type(value1) == 2 and category_type(value2) == 1:
        # form 2
        frame.stack.append(value1)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    value3 = frame.stack.pop()
    if (category_type(value1) == 1 and category_type(value2) == 1 and
            category_type(value3) == 1):
        # form 1
        frame.stack.append(value2)
        frame.stack.append(value1)
        frame.stack.append(value3)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    assert False  # should never get here


@bytecode(code=0x5e)
def dup2_x2(frame):
    value1 = frame.stack.pop()
    value2 = frame.stack.pop()
    if category_type(value1) == 2 and category_type(value2) == 2:
        # form 4
        frame.stack.append(value1)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    value3 = frame.stack.pop()
    if (category_type(value1) == 1 and category_type(value2) == 1 and
            category_type(value3) == 2):
        # form 3
        frame.stack.append(value2)
        frame.stack.append(value1)
        frame.stack.append(value3)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    if (category_type(value1) == 2 and category_type(value2) == 1 and
            category_type(value3) == 1):
        # form 2
        frame.stack.append(value1)
        frame.stack.append(value3)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    value4 = frame.stack.pop()
    if (category_type(value1) == 1 and category_type(value2) == 1 and
            category_type(value3) == 1 and category_type(value4) == 1):
        # form 1
        frame.stack.append(value2)
        frame.stack.append(value1)
        frame.stack.append(value4)
        frame.stack.append(value3)
        frame.stack.append(value2)
        frame.stack.append(value1)
        return
    assert False  # should never get here


@bytecode(code=0x5f)
def swap(frame):
    value1 = frame.stack.pop()
    value2 = frame.stack.pop()
    frame.stack.append(value2)
    frame.stack.append(value1)


@bytecode(code=0xa9)
def ret(frame):
    index = struct.unpack(">B", frame.code[frame.pc])[0]
    frame.pc = frame.args[index]


@bytecode(code=0xba)
def invokedynamic(frame):
    raise Exception("Method handlers are not supported")


@bytecode(code=0xca)
def breakpoint(frame):
    raise Exception("This op code (fe) should not present in class file")


@bytecode(code=0xc2)
def monitorenter(frame):
    ref = frame.stack.pop()
    jassert_ref(ref)
    o = frame.vm.heap[ref[1]]
    if "@monitor" in o.fields:
        if o.fields["@monitor"] == frame.thread:
            o.fields["@monitor_count"] += 1
        else:
            frame.stack.append(ref)
            raise SkipThreadCycle()
    else:
        o.fields["@monitor"] = frame.thread
        o.fields["@monitor_count"] = 1


@bytecode(code=0xc3)
def monitorexit(frame):
    ref = frame.stack.pop()
    jassert_ref(ref)
    o = frame.vm.heap[ref[1]]
    if o.fields["@monitor_count"] == 1:
        del o.fields["@monitor"]
        del o.fields["@monitor_count"]
    else:
        o.fields["@monitor_count"] -= 1


@bytecode(code=0xc4)
def wide(frame):
    op_code = ord(frame.code[frame.pc])
    frame.pc += 1
    data = frame.code[frame.pc:frame.pc + 2]
    index = struct.unpack(">H", data)[0]
    frame.pc += 2
    if op_code == 132:  # x84 iinc
        data = frame.code[frame.pc:frame.pc + 2]
        value = struct.unpack(">h", data)[0]
        frame.pc += 2
        assert type(frame.args[index]) is int
        frame.args[index] += value
        return
    if op_code in (0x15, 0x16, 0x17, 0x18, 0x19):
        # *load
        frame.stack.append(frame.args[index])
        return
    if op_code in (0x36, 0x37, 0x38, 0x39, 0x3a):
        # *store
        frame.stack.append(frame.args[index])
        return
    if op_code == 0xa9:
        # ret
        frame.pc = frame.args[index]
        return
    assert False  # should never get here


@bytecode(code=0xfe)
def impdep1(frame):
    raise Exception("This op code (fe) should not present in class file")


@bytecode(code=0xff)
def impdep2(frame):
    raise Exception("This op code (ff) should not present in class file")
