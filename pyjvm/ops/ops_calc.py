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


def op_0x60(frame):  # iadd
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1 + value2
    result = cut_to_int(result)
    jassert_int(result)
    frame.stack.append(result)


def op_0x61(frame):  # ladd
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1[1] + value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


def op_0x62(frame):  # fadd
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    result = value1[1] + value2[1]
    frame.stack.append(("float", result))


def op_0x63(frame):  # dadd
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    result = value1[1] + value2[1]
    frame.stack.append(("double", result))


def op_0x64(frame):  # isub
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1 - value2
    result = cut_to_int(result)
    frame.stack.append(result)


def op_0x65(frame):  # lsub
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1[1] - value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


def op_0x66(frame):  # fsub
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    result = value1[1] - value2[1]
    frame.stack.append(("float", result))


def op_0x67(frame):  # dsub
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    result = value1[1] - value2[1]
    frame.stack.append(("double", result))


def op_0x68(frame):  # imul
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1 * value2
    result = cut_to_int(result)
    frame.stack.append(result)


def op_0x69(frame):  # lmul
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    result = value1[1] * value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


def op_0x6a(frame):  # fmul
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    result = value1[1] * value2[1]
    #result = numpy.float32(result)
    frame.stack.append(("float", result))


def op_0x6b(frame):  # dmul
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    result = value1[1] * value2[1]
    frame.stack.append(("double", result))


def op_0x6c(frame):  # idiv
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    if value2 == 0:
        frame.vm.raise_exception(frame, "java/lang/ArithmeticException")
        return
    result = int(float(value1) / value2)
    result = cut_to_int(result)
    frame.stack.append(result)


def op_0x6d(frame):  # ldiv
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


def op_0x6e(frame):  # fdiv
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_float(value1)
    jassert_float(value2)
    if value2[1] == 0:
        frame.stack.append(("float", float("inf")))
        return
    result = value1[1] / value2[1]
    frame.stack.append(("float", result))


def op_0x6f(frame):  # ddiv
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_double(value1)
    jassert_double(value2)
    if value2[1] == 0:
        frame.stack.append(("double", float("inf")))
        return
    result = value1[1] / value2[1]
    frame.stack.append(("double", result))


def op_0x70(frame):  # irem
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    if value2 == 0:
        frame.vm.raise_exception(frame, "java/lang/ArithmeticException")
        return
    result = value1 % value2
    result = cut_to_int(result)
    frame.stack.append(result)


def op_0x71(frame):  # lrem
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


def op_0x72(frame):  # frem
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    frame.stack.append(0)  # hardcoded for now


def op_0x73(frame):  # drem
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    frame.stack.append(0)  # hardcoded for now


def op_0x74(frame):  # ineg
    value = frame.stack.pop()
    result = value * -1
    result = cut_to_int(result)
    frame.stack.append(result)


def op_0x75(frame):  # lneg
    value = frame.stack.pop()
    jassert_long(value)
    result = value[1] * -1
    result = cut_to_long(result)
    frame.stack.append(("long", long(result)))


def op_0x76(frame):  # fneg
    value = frame.stack.pop()
    jassert_double(value)
    result = value[1] * -1
    frame.stack.append(("float", result))


def op_0x77(frame):  # dneg
    value = frame.stack.pop()
    jassert_double(value)
    result = value[1] * -1
    frame.stack.append(("double", result))


def op_0x83(frame):  # lxor
    value2 = frame.stack.pop()
    value1 = frame.stack.pop()
    jassert_long(value1)
    jassert_long(value2)
    result = value1[1] ^ value2[1]
    result = cut_to_long(result)
    frame.stack.append(("long", result))


def op_0x84(frame):  # iinc
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    vconst = struct.unpack('b', frame.code[frame.pc])[0]
    frame.pc += 1
    result = frame.args[index] + vconst
    result = cut_to_int(result)
    frame.args[index] = result
