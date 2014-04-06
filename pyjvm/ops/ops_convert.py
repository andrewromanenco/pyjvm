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

import math
import struct

from pyjvm.jassert import jassert_float
from pyjvm.jassert import jassert_double
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long


def op_0x85(frame):  # i2l
    value = frame.stack.pop()
    jassert_int(value)
    value = long(value)  # no real need
    frame.stack.append(("long", value))


def op_0x86(frame):  # i2f
    value = frame.stack.pop()
    jassert_int(value)
    frame.stack.append(("float", float(value)))


def op_0x87(frame):  # i2d
    value = frame.stack.pop()
    jassert_int(value)
    frame.stack.append(("double", float(value)))


def op_0x88(frame):  # l2i
    value = frame.stack.pop()
    jassert_long(value)
    data = struct.pack(">q", value[1])
    data = data[4:]
    result = struct.unpack(">i", data)[0]
    jassert_int(result)
    frame.stack.append(result)


def op_0x89(frame):  # l2f
    value = frame.stack.pop()
    jassert_long(value)
    result = ("float", float(value[1]))
    frame.stack.append(result)


def op_0x8a(frame):  # l2d
    value = frame.stack.pop()
    jassert_long(value)
    result = ("double", float(value[1]))
    frame.stack.append(result)


def op_0x8b(frame):  # f2i
    value = frame.stack.pop()
    jassert_float(value)
    if value[1] is None:
        frame.stack.append(0)
    else:
        if value[1] < -2147483648:  # -1 * math.pow(2, 31)
            result = -2147483648
        elif value[1] > 2147483647:  # math.pow(2, 31) - 1
            result = 2147483647
        else:
            result = int(value[1])
        jassert_int(result)
        frame.stack.append(result)


def op_0x8c(frame):  # f2l
    value = frame.stack.pop()
    jassert_float(value)
    if value[1] is None:
        frame.stack.append(("long", 0))
    else:
        min_value = long(-1 * math.pow(2, 63))
        max_value = long(math.pow(2, 63) - 1)
        if value[1] < min_value:
            result = min_value
        elif value[1] > max_value:
            result = max_value
        else:
            result = long(value[1])
        jassert_long(("long", result))
        frame.stack.append(("long", result))


def op_0x8d(frame):  # f2d
    value = frame.stack.pop()
    jassert_float(value)
    frame.stack.append(("double", value[1]))


def op_0x8e(frame):  # d2i
    value = frame.stack.pop()
    jassert_double(value)
    if value[1] is None:
        frame.stack.append(0)
    else:
        if value[1] < -2147483648:  # -1 * math.pow(2, 31)
            result = -2147483648
        elif value[1] > 2147483647:  # math.pow(2, 31) - 1
            result = 2147483647
        else:
            result = int(value[1])
        jassert_int(result)
        frame.stack.append(result)


def op_0x8f(frame):  # d2l
    value = frame.stack.pop()
    jassert_double(value)
    if value[1] is None:
        frame.stack.append(("long", 0))
    else:
        min_value = long(-1 * math.pow(2, 63))
        max_value = long(math.pow(2, 63) - 1)
        if value[1] < min_value:
            result = min_value
        elif value[1] > max_value:
            result = max_value
        else:
            result = long(value[1])
        jassert_long(("long", result))
        frame.stack.append(("long", result))


def op_0x90(frame):  # d2f
    value = frame.stack.pop()
    jassert_double(value)
    frame.stack.append(("float", value[1]))


def op_0x91(frame):  # i2b
    value = frame.stack.pop()
    jassert_int(value)
    data = struct.pack(">i", value)
    data = data[3]
    result = struct.unpack(">b", data)[0]
    frame.stack.append(result)


def op_0x92(frame):  # i2c
    value = frame.stack.pop()
    jassert_int(value)
    data = struct.pack(">i", value)
    data = data[2:]
    result = struct.unpack(">H", data)[0]
    assert type(result) is int
    assert 0 <= result <= int(math.pow(2, 16))
    frame.stack.append(result)


def op_0x93(frame):  # i2s
    value = frame.stack.pop()
    jassert_int(value)
    data = struct.pack(">i", value)
    data = data[2:]
    result = struct.unpack(">h", data)[0]
    assert type(result) is int
    frame.stack.append(result)
