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

from pyjvm.bytecode import bytecode
from pyjvm.frame import Frame
from pyjvm.natives import exec_native
from pyjvm.thread import SkipThreadCycle
from pyjvm.utils import args_count
from pyjvm.vmo import VM_OBJECTS

logger = logging.getLogger(__name__)


@bytecode(code=0xb8)
def invokestatic(frame):
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_methodref = frame.this_class.constant_pool[index]
    assert cp_methodref[0] == 10  # CONSTANT_Methodref
    klass_info = frame.this_class.constant_pool[cp_methodref[1]]
    assert klass_info[0] == 7  # CONSTANT_Class_info
    name_and_type = frame.this_class.constant_pool[cp_methodref[2]]
    assert name_and_type[0] == 12  # name_and_type_index
    klass_name = frame.this_class.constant_pool[klass_info[1]][1]
    method_name = frame.this_class.constant_pool[name_and_type[1]][1]
    method_signature = frame.this_class.constant_pool[name_and_type[2]][1]
    assert klass_name is not None
    assert method_name is not None
    assert method_signature is not None

    if klass_name == "sun/misc/VM" and method_name == "isBooted":
        # shortcut, to be remvoed
        frame.stack.append(1)
        return

    if (klass_name == "sun/reflect/Reflection" and
            method_name == "registerMethodsToFilter"):
        logger.debug("Ignoring registerMethodsToFilter")
        frame.stack.pop()
        frame.stack.pop()
        return

    if (klass_name == "sun/misc/SharedSecrets" and
            method_name == "getJavaLangAccess"):
        # use vm owned object instead of constructing real one
        frame.vm.get_class("sun/misc/JavaLangAccess")
        frame.stack.append(("vm_ref", VM_OBJECTS["JavaLangAccess"]))
        return

    logger.debug("%s %s %s", klass_name, method_name, method_signature)

    klass = frame.vm.get_class(klass_name)
    method = klass.find_method(method_name, method_signature)
    assert method is not None
    assert method[0] & 0x0008 > 0  # make sure this is static method

    obj_mon = None
    if method[0] & 0x0020:
        obj_mon = frame.vm.heap[klass.heap_ref[1]]
        if "@monitor" in obj_mon.fields:
            if obj_mon.fields["@monitor"] == frame.thread:
                obj_mon.fields["@monitor_count"] += 1
            else:
                raise SkipThreadCycle()
        else:
            obj_mon.fields["@monitor"] = frame.thread
            obj_mon.fields["@monitor_count"] = 1

    nargs = args_count(method_signature)
    args = [None] * nargs
    while nargs > 0:
        value = frame.stack.pop()
        if type(value) is tuple and value[0] in ('long', 'double'):
            nargs -= 1
        args[nargs - 1] = value
        nargs -= 1

    if method[0] & 0x0100 > 0:  # is native?
        exec_native(frame, args, klass, method_name, method_signature)
        return

    m_args = [''] * method[1]
    m_args[0:len(args)] = args[0:len(args)]

    logger.debug("InvStatic: %s %s in %s", method_name, method_signature,
                 klass_name)
    if method_name == "countBits":
        frame.stack.append(5)
        return

    sub = Frame(frame.thread, klass, method, m_args,
                "InvStatic: %s %s in %s" % (method_name, method_signature,
                                            klass_name))
    if obj_mon is not None:
        sub.monitor = obj_mon
    frame.thread.frame_stack.append(sub)
