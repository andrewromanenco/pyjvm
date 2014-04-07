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
from pyjvm.jassert import jassert_float
from pyjvm.jassert import jassert_double
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long
from pyjvm.jassert import jassert_ref

logger = logging.getLogger(__name__)


@bytecode(code=0x0)
def nop(frame):
    # BEST OP CODE, yes - it asks to do nothing
    pass


@bytecode(code=0x1)
def aconst_null(frame):
    frame.stack.append(None)


@bytecode(code=0x2)
def iconst_m1(frame):
    frame.stack.append(-1)


@bytecode(code=0x3)
def iconst_0(frame):
    frame.stack.append(0)


@bytecode(code=0x4)
def iconst_1(frame):
    frame.stack.append(1)


@bytecode(code=0x5)
def iconst_2(frame):
    frame.stack.append(2)


@bytecode(code=0x6)
def iconst_3(frame):
    frame.stack.append(3)


@bytecode(code=0x7)
def iconst_4(frame):
    frame.stack.append(4)


@bytecode(code=0x8)
def iconst_5(frame):
    frame.stack.append(5)


@bytecode(code=0x9)
def lconst_0(frame):
    frame.stack.append(("long", 0))


@bytecode(code=0xa)
def lconst_1(frame):
    frame.stack.append(("long", 1))


@bytecode(code=0xb)
def fconst_0(frame):
    frame.stack.append(("float", 0.0))


@bytecode(code=0xc)
def fconst_1(frame):
    frame.stack.append(("float", 1.0))


@bytecode(code=0xd)
def fconst_2(frame):
    frame.stack.append(("float", 2.0))


@bytecode(code=0xe)
def dconst_0(frame):
    frame.stack.append(("double", 0.0))


@bytecode(code=0xf)
def dconst_1(frame):
    frame.stack.append(("double", 1.0))


@bytecode(code=0x10)
def bipush(frame):
    byte = frame.code[frame.pc]
    frame.pc += 1
    value = struct.unpack(">b", byte)[0]
    frame.stack.append(value)


@bytecode(code=0x11)
def sipush(frame):
    short = struct.unpack(">h", frame.code[frame.pc]
                          + frame.code[frame.pc + 1])[0]
    frame.pc += 2
    frame.stack.append(short)


@bytecode(code=0x12)
def ldc(frame):
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


@bytecode(code=0x13)
def ldc_w(frame):
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


@bytecode(code=0x14)
def ldc2_w(frame):
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


@bytecode(code=0x15)
def iload(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_int(value)
    frame.stack.append(value)


@bytecode(code=0x16)
def lload(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_long(value)
    frame.stack.append(value)


@bytecode(code=0x17)
def fload(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_float(value)
    frame.stack.append(value)


@bytecode(code=0x18)
def dload(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_double(value)
    frame.stack.append(value)


@bytecode(code=0x19)
def aload(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.args[index]
    jassert_ref(value)
    frame.stack.append(value)


@bytecode(code=0x1a)
def iload_0(frame):
    value = frame.args[0]
    jassert_int(value)
    frame.stack.append(value)


@bytecode(code=0x1b)
def iload_1(frame):
    value = frame.args[1]
    jassert_int(value)
    frame.stack.append(value)


@bytecode(code=0x1c)
def iload_2(frame):
    value = frame.args[2]
    jassert_int(value)
    frame.stack.append(value)


@bytecode(code=0x1d)
def iload_3(frame):
    value = frame.args[3]
    jassert_int(value)
    frame.stack.append(value)


@bytecode(code=0x1e)
def lload_0(frame):
    value = frame.args[0]
    jassert_long(value)
    frame.stack.append(value)


@bytecode(code=0x1f)
def lload_1(frame):
    value = frame.args[1]
    jassert_long(value)
    frame.stack.append(value)


@bytecode(code=0x20)
def lload_2(frame):
    value = frame.args[2]
    jassert_long(value)
    frame.stack.append(value)


@bytecode(code=0x21)
def lload_3(frame):
    value = frame.args[3]
    jassert_long(value)
    frame.stack.append(value)


@bytecode(code=0x22)
def fload_0(frame):
    value = frame.args[0]
    jassert_float(value)
    frame.stack.append(value)


@bytecode(code=0x23)
def fload_1(frame):
    value = frame.args[1]
    jassert_float(value)
    frame.stack.append(value)


@bytecode(code=0x24)
def fload_2(frame):
    value = frame.args[2]
    jassert_float(value)
    frame.stack.append(value)


@bytecode(code=0x25)
def fload_3(frame):
    value = frame.args[3]
    jassert_float(value)
    frame.stack.append(value)


@bytecode(code=0x26)
def dload_0(frame):
    value = frame.args[0]
    jassert_double(value)
    frame.stack.append(value)


@bytecode(code=0x27)
def dload_1(frame):
    value = frame.args[1]
    jassert_double(value)
    frame.stack.append(value)


@bytecode(code=0x28)
def dload_2(frame):
    value = frame.args[2]
    jassert_double(value)
    frame.stack.append(value)


@bytecode(code=0x29)
def dload_3(frame):
    value = frame.args[3]
    jassert_double(value)
    frame.stack.append(value)


@bytecode(code=0x2a)
def aload_0(frame):
    value = frame.args[0]
    jassert_ref(value)
    frame.stack.append(value)


@bytecode(code=0x2b)
def aload_1(frame):
    value = frame.args[1]
    jassert_ref(value)
    frame.stack.append(value)


@bytecode(code=0x2c)
def aload_2(frame):
    value = frame.args[2]
    jassert_ref(value)
    frame.stack.append(value)


@bytecode(code=0x2d)
def aload_3(frame):
    value = frame.args[3]
    jassert_ref(value)
    frame.stack.append(value)


@bytecode(code=0x36)
def istore(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[index] = value


@bytecode(code=0x37)
def lstore(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[index] = value


@bytecode(code=0x38)
def fstore(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[index] = value


@bytecode(code=0x39)
def dstore(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[index] = value


@bytecode(code=0x3a)
def astore(frame):
    index = ord(frame.code[frame.pc])
    frame.pc += 1
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[index] = value


@bytecode(code=0x3b)
def istore_0(frame):
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[0] = value


@bytecode(code=0x3c)
def istore_1(frame):
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[1] = value


@bytecode(code=0x3d)
def istore_2(frame):
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[2] = value


@bytecode(code=0x3e)
def istore_3(frame):
    value = frame.stack.pop()
    jassert_int(value)
    frame.args[3] = value


@bytecode(code=0x3f)
def lstore_0(frame):
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[0] = value


@bytecode(code=0x40)
def lstore_1(frame):
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[1] = value


@bytecode(code=0x41)
def lstore_2(frame):
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[2] = value


@bytecode(code=0x42)
def lstore_3(frame):
    value = frame.stack.pop()
    jassert_long(value)
    frame.args[3] = value


@bytecode(code=0x43)
def fstore_0(frame):
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[0] = value


@bytecode(code=0x44)
def fstore_1(frame):
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[1] = value


@bytecode(code=0x45)
def fstore_2(frame):
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[2] = value


@bytecode(code=0x46)
def fstore_3(frame):
    value = frame.stack.pop()
    jassert_float(value)
    frame.args[3] = value


@bytecode(code=0x47)
def dstore_0(frame):
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[0] = value


@bytecode(code=0x48)
def dstore_1(frame):
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[1] = value


@bytecode(code=0x49)
def dstore_2(frame):
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[2] = value


@bytecode(code=0x4a)
def dstore_3(frame):
    value = frame.stack.pop()
    jassert_double(value)
    frame.args[3] = value


@bytecode(code=0x4b)
def astore_0(frame):
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[0] = value


@bytecode(code=0x4c)
def astore_1(frame):
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[1] = value


@bytecode(code=0x4d)
def astore_2(frame):
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[2] = value


@bytecode(code=0x4e)
def astore_3(frame):
    value = frame.stack.pop()
    jassert_ref(value)
    frame.args[3] = value
