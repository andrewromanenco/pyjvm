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
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long
from pyjvm.ops.ops_calc import cut_to_int
from pyjvm.ops.ops_calc import cut_to_long


def rshift(val, n):
    return (val % 0x100000000) >> n


@bytecode(code=0x78)
def ishl(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value2)
    jassert_int(value1)
    value2 &= 0b11111
    result = value1 << value2
    result = cut_to_int(result)
    jassert_int(result)
    frame.stack.append(result)


@bytecode(code=0x79)
def lshl(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value2)
    jassert_long(value1)
    value2 &= 0b111111
    result = value1[1] << value2
    result = ("long", cut_to_long(result))
    jassert_long(result)
    frame.stack.append(result)


@bytecode(code=0x7a)
def ishr(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value2)
    jassert_int(value1)
    value2 &= 0b11111
    result = value1 >> value2
    result = cut_to_int(result)
    jassert_int(result)
    frame.stack.append(result)


@bytecode(code=0x7b)
def lshr(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value2)
    jassert_long(value1)
    value2 &= 0b111111
    result = value1[1] >> value2
    result = ("long", cut_to_long(result))
    jassert_long(result)
    frame.stack.append(result)


@bytecode(code=0x7c)
def iushr(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value2)
    jassert_int(value1)
    value2 &= 0b11111
    data = struct.pack(">i", value1)
    result = struct.unpack(">I", data)[0]
    result >>= value2
    data = struct.pack(">I", result)
    result = struct.unpack(">i", data)[0]
    jassert_int(value1)
    frame.stack.append(result)


@bytecode(code=0x7d)
def lushr(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_long(value1)
    jassert_int(value2)
    value2 &= 0b111111
    data = struct.pack(">q", value1[1])
    result = struct.unpack(">Q", data)[0]
    result >>= value2
    data = struct.pack(">Q", result)
    result = struct.unpack(">q", data)[0]
    result = ("long", cut_to_long(result))
    jassert_long(result)
    frame.stack.append(result)


@bytecode(code=0x7e)
def iand(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value2)
    jassert_int(value1)
    result = value1 & value2
    result = cut_to_int(result)
    jassert_int(result)
    frame.stack.append(result)


@bytecode(code=0x7f)
def land(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_long(value2)
    jassert_long(value1)
    result = value1[1] & value2[1]
    result = ("long", cut_to_int(result))
    jassert_long(result)
    frame.stack.append(result)


@bytecode(code=0x80)
def ior(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value2)
    jassert_int(value1)
    result = value1 | value2
    result = cut_to_int(result)
    jassert_int(result)
    frame.stack.append(result)


@bytecode(code=0x81)
def lor(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_long(value2)
    jassert_long(value1)
    result = value1[1] | value2[1]
    result = ("long", cut_to_int(result))
    jassert_long(result)
    frame.stack.append(result)


@bytecode(code=0x82)
def ixor(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_int(value2)
    jassert_int(value1)
    result = value1 ^ value2
    result = cut_to_int(result)
    jassert_int(result)
    frame.stack.append(result)
