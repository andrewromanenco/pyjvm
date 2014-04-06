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

from pyjvm.jassert import jassert_float
from pyjvm.jassert import jassert_double
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long
from pyjvm.jassert import jassert_ref

logger = logging.getLogger(__name__)


def op_0x0(frame):  # nop
    # BEST OP CODE, yes - it asks to do nothing
    pass


def op_0x1(frame):  # aconst_null
    frame.stack.append(None)


def op_0x2(frame):  # iconst_m1
    frame.stack.append(-1)


def op_0x3(frame):  # iconst_0
    frame.stack.append(0)


def op_0x4(frame):  # iconst_1
    frame.stack.append(1)


def op_0x5(frame):  # iconst_2
    frame.stack.append(2)


def op_0x6(frame):  # iconst_3
    frame.stack.append(3)


def op_0x7(frame):  # iconst_4
    frame.stack.append(4)


def op_0x8(frame):  # iconst_5
    frame.stack.append(5)


def op_0x9(frame):  # lconst_0
    frame.stack.append(("long", 0))


def op_0xa(frame):  # lconst_1
    frame.stack.append(("long", 1))


def op_0xb(frame):  # fconst_0
    frame.stack.append(("float", 0.0))


def op_0xc(frame):  # fconst_1
    frame.stack.append(("float", 1.0))


def op_0xd(frame):  # fconst_2
    frame.stack.append(("float", 2.0))


def op_0xe(frame):  # dconst_0
    frame.stack.append(("double", 0.0))


def op_0xf(frame):  # dconst_1
    frame.stack.append(("double", 1.0))


def op_0x10(frame):  # bipush: byte to int
    byte = frame.code[frame.pc]
    frame.pc += 1
    value = struct.unpack(">b", byte)[0]
    frame.stack.append(value)


def op_0x11(frame):  # sipush: byte to int
    short = struct.unpack(">h", frame.code[frame.pc]
                          + frame.code[frame.pc + 1])[0]
    frame.pc += 2
    frame.stack.append(short)


def op_0x12(frame):  # ldc: Str, int, float to stack
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    cp_item = frame.this_class.constant_pool[index]
    if cp_item[0] == 8:  # CONSTANT_String
        value = frame.this_class.constant_pool[cp_item[1]][1]
        ref = frame.vm.make_heap_string(value)
        frame.stack.append(ref)
        return
    elif cp_item[0] == 3:  # CONSTANT_Int
        frame.stack.append(cp_item[1])
        return
    elif cp_item[0] == 4:  # CONSTANT_Float
        frame.stack.append(("float", cp_item[1]))
        return
    elif cp_item[0] == 7:  # CONSTANT_Class
        klass_name = frame.this_class.constant_pool[cp_item[1]][1]
        logger.debug(klass_name)
        klass = frame.vm.get_class(klass_name)
        frame.stack.append(klass.heap_ref)
        return
    else:
        # No support for method ref
        raise Exception("0x12 not yet supported cp item type: %d" % cp_item[0])


def op_0x13(frame):  # ldc_w: Str, int, float to stack
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_item = frame.this_class.constant_pool[index]
    if cp_item[0] == 7:  # CONSTANT_Class
        klass_name = frame.this_class.constant_pool[cp_item[1]][1]
        logger.debug(klass_name)
        klass = frame.vm.get_class(klass_name)
        frame.stack.append(klass.heap_ref)
        return
    elif cp_item[0] == 8:  # CONSTANT_String
        value = frame.this_class.constant_pool[cp_item[1]][1]
        ref = frame.vm.make_heap_string(value)
        frame.stack.append(ref)
        return
    elif cp_item[0] == 4:  # CONSTANT_Float
        frame.stack.append(("float", cp_item[1]))
        return
    elif cp_item[0] == 3:  # CONSTANT_Int
        frame.stack.append(cp_item[1])
        return
    else:
        # No support for method ref yet
        raise Exception("0x13 not yet supported cp item type: %d" % cp_item[0])


def op_0x14(frame):  # ldc2_w
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_item = frame.this_class.constant_pool[index]
    if cp_item[0] == 6:  # double
        frame.stack.append(("double", cp_item[1]))
    elif cp_item[0] == 5:  # long
        frame.stack.append(("long", cp_item[1]))
    else:
        # This should never happen
        raise Exception(cp_item)


def op_0x15(frame):  # iload
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_int(value)
    frame.stack.append(value)


def op_0x16(frame):  # lload
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_long(value)
    frame.stack.append(value)


def op_0x17(frame):  # fload
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_float(value)
    frame.stack.append(value)


def op_0x18(frame):  # dload
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_double(value)
    frame.stack.append(value)


def op_0x19(frame):  # aload
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_ref(value)
    frame.stack.append(value)


def op_0x1a(frame):  # iload_0
    value = frame.args[0]
    jassert_int(value)
    frame.stack.append(value)


def op_0x1b(frame):  # iload_1
    value = frame.args[1]
    jassert_int(value)
    frame.stack.append(value)


def op_0x1c(frame):  # iload_2
    value = frame.args[2]
    jassert_int(value)
    frame.stack.append(value)


def op_0x1d(frame):  # iload_3
    value = frame.args[3]
    jassert_int(value)
    frame.stack.append(value)


def op_0x1e(frame):  # lload_0
    value = frame.args[0]
    jassert_long(value)
    frame.stack.append(value)


def op_0x1f(frame):  # lload_1
    value = frame.args[1]
    jassert_long(value)
    frame.stack.append(value)


def op_0x20(frame):  # lload_2
    value = frame.args[2]
    jassert_long(value)
    frame.stack.append(value)


def op_0x21(frame):  # lload_3
    value = frame.args[3]
    jassert_long(value)
    frame.stack.append(value)


def op_0x22(frame):  # fload_0
    value = frame.args[0]
    jassert_float(value)
    frame.stack.append(value)


def op_0x23(frame):  # fload_1
    value = frame.args[1]
    jassert_float(value)
    frame.stack.append(value)


def op_0x24(frame):  # fload_2
    value = frame.args[2]
    jassert_float(value)
    frame.stack.append(value)


def op_0x25(frame):  # fload_3
    value = frame.args[3]
    jassert_float(value)
    frame.stack.append(value)


def op_0x26(frame):  # dload_0
    value = frame.args[0]
    jassert_double(value)
    frame.stack.append(value)


def op_0x27(frame):  # dload_1
    value = frame.args[1]
    jassert_double(value)
    frame.stack.append(value)


def op_0x28(frame):  # dload_2
    value = frame.args[2]
    jassert_double(value)
    frame.stack.append(value)


def op_0x29(frame):  # dload_3
    value = frame.args[3]
    jassert_double(value)
    frame.stack.append(value)


def op_0x2a(frame):  # aload_0
    value = frame.args[0]
    jassert_ref(value)
    frame.stack.append(value)


def op_0x2b(frame):  # aload_1
    value = frame.args[1]
    jassert_ref(value)
    frame.stack.append(value)


def op_0x2c(frame):  # aload_2
    value = frame.args[2]
    jassert_ref(value)
    frame.stack.append(value)


def op_0x2d(frame):  # aload_3
    value = frame.args[3]
    jassert_ref(value)
    frame.stack.append(value)


def op_0x36(frame):  # istore
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[index] = value


def op_0x37(frame):  # lstore
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[index] = value


def op_0x38(frame):  # fstore
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[index] = value


def op_0x39(frame):  # dstore
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[index] = value


def op_0x3a(frame):  # astore
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[index] = value


def op_0x3b(frame):  # istore_0
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[0] = value


def op_0x3c(frame):  # istore_1
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[1] = value


def op_0x3d(frame):  # istore_2
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[2] = value


def op_0x3e(frame):  # istore_3
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[3] = value


def op_0x3f(frame):  # lstore_0
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[0] = value


def op_0x40(frame):  # lstore_1
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[1] = value


def op_0x41(frame):  # lstore_2
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[2] = value


def op_0x42(frame):  # lstore_3
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[3] = value


def op_0x43(frame):  # fstore_0
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[0] = value


def op_0x44(frame):  # fstore_1
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[1] = value


def op_0x45(frame):  # fstore_2
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[2] = value


def op_0x46(frame):  # fstore_3
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[3] = value


def op_0x47(frame):  # dstore_0
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[0] = value


def op_0x48(frame):  # dstore_1
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[1] = value


def op_0x49(frame):  # dstore_2
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[2] = value


def op_0x4a(frame):  # dstore_3
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[3] = value


def op_0x4b(frame):  # astore_0
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[0] = value


def op_0x4c(frame):  # astore_1
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[1] = value


def op_0x4d(frame):  # astore_2
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[2] = value


def op_0x4e(frame):  # astore_3
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[3] = value
