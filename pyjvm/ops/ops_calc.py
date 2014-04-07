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
import struct

from pyjvm.bytecode import bytecode
from pyjvm.jassert import jassert_double
from pyjvm.jassert import jassert_float
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long

logger = logging.getLogger(__name__)

FLAG32 = 1 << 31
FLAG64 = 1 << 63


def cut_to_int(value):
    if -2147483648 <= value <= 2147483647:
        return int(value)
    if value & FLAG32:
        value &= 0xFFFFFFFF
        value ^= 0xFFFFFFFF
        value += 1
        value *= -1
    else:
        value &= 0xFFFFFFFF
    jassert_int(value)
    return int(value)


def cut_to_long(value):
    if -9223372036854775808 <= value <= 9223372036854775807:
        return long(value)
    if value & FLAG64:
        value &= 0xFFFFFFFFFFFFFFFF
        value ^= 0xFFFFFFFFFFFFFFFF
        value += 1
        value *= -1
    else:
        value &= 0xFFFFFFFFFFFFFFFF
    jassert_long(("long", value))
    return long(value)


@bytecode(code=0x60)
def iadd(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1 + value2
    result = cut_to_int(result)
    jassert_int(result)
    frame.stack.append(result)


@bytecode(code=0x61)
def ladd(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1[1] + value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


@bytecode(code=0x62)
def fadd(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    result = value1[1] + value2[1]
    frame.stack.append(("float", result))


@bytecode(code=0x63)
def dadd(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    result = value1[1] + value2[1]
    frame.stack.append(("double", result))


@bytecode(code=0x64)
def isub(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1 - value2
    result = cut_to_int(result)
    frame.stack.append(result)


@bytecode(code=0x65)
def lsub(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1[1] - value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


@bytecode(code=0x66)
def fsub(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    result = value1[1] - value2[1]
    frame.stack.append(("float", result))


@bytecode(code=0x67)
def dsub(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    result = value1[1] - value2[1]
    frame.stack.append(("double", result))


@bytecode(code=0x68)
def imul(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1 * value2
    result = cut_to_int(result)
    frame.stack.append(result)


@bytecode(code=0x69)
def lmul(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1[1] * value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


@bytecode(code=0x6a)
def fmul(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    result = value1[1] * value2[1]
    #result = numpy.float32(result)
    frame.stack.append(("float", result))


@bytecode(code=0x6b)
def dmul(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    result = value1[1] * value2[1]
    frame.stack.append(("double", result))


@bytecode(code=0x6c)
def idiv(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    if value2 == 0:
        frame.vm.raise_exception(frame, "java/lang/ArithmeticException")
        return
    result = int(float(value1) / value2)
    result = cut_to_int(result)
    frame.stack.append(result)


@bytecode(code=0x6d)
def ldiv(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_long(value1)
    jassert_long(value2)
    if value2[1] == 0:
        frame.vm.raise_exception(frame, "java/lang/ArithmeticException")
        return
    result = abs(value1[1]) / abs(value2[1])
    if (value1[1] < 0 and value2[1] > 0) or (value1[1] > 0 and value2[1] < 0):
        result *= -1
    #result = long(float(value1[1]) / value2[1]) - this will overflow
    result = cut_to_long(result)
    frame.stack.append(("long", long(result)))


@bytecode(code=0x6e)
def fdiv(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    if value2[1] == 0:
        frame.stack.append(("float", float("inf")))
        return
    result = value1[1] / value2[1]
    frame.stack.append(("float", result))


@bytecode(code=0x6f)
def ddiv(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    if value2[1] == 0:
        frame.stack.append(("double", float("inf")))
        return
    result = value1[1] / value2[1]
    frame.stack.append(("double", result))


@bytecode(code=0x70)
def irem(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    if value2 == 0:
        frame.vm.raise_exception(frame, "java/lang/ArithmeticException")
        return
    result = value1 % value2
    result = cut_to_int(result)
    frame.stack.append(result)


@bytecode(code=0x71)
def lrem(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_long(value1)
    jassert_long(value2)
    if value2[1] == 0:
        frame.vm.raise_exception(frame, "java/lang/ArithmeticException")
        return
    result = value1[1] % value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


@bytecode(code=0x72)
def frem(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    frame.stack.append(0)  # hardcoded for now


@bytecode(code=0x73)
def drem(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    frame.stack.append(0)  # hardcoded for now


@bytecode(code=0x74)
def ineg(frame):
    value = frame.stack.pop()
    result = value * -1
    result = cut_to_int(result)
    frame.stack.append(result)


@bytecode(code=0x75)
def lneg(frame):
    value = frame.stack.pop()
    jassert_long(value)
    result = value[1] * -1
    result = cut_to_long(result)
    frame.stack.append(("long", long(result)))


@bytecode(code=0x76)
def fneg(frame):
    value = frame.stack.pop()
    jassert_double(value)
    result = value[1] * -1
    frame.stack.append(("float", result))


@bytecode(code=0x77)
def dneg(frame):
    value = frame.stack.pop()
    jassert_double(value)
    result = value[1] * -1
    frame.stack.append(("double", result))


@bytecode(code=0x83)
def lxor(frame):
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_long(value1)
    jassert_long(value2)
    result = value1[1] ^ value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


@bytecode(code=0x84)
def iinc(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    vconst = struct.unpack('b', frame.code[frame.pc])[0]
    frame.pc += 1
    result = frame.args[index] + vconst
    result = cut_to_int(result)
    frame.args[index] = result
