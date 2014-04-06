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

from pyjvm.frame import Frame
from pyjvm.jassert import jassert_ref
from pyjvm.natives import exec_native
from pyjvm.thread import SkipThreadCycle
from pyjvm.utils import args_count

logger = logging.getLogger(__name__)


def op_0xb7(frame):  # invokespecial
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_item = frame.this_class.constant_pool[index]
    assert cp_item[0] == 10  # CONSTANT_Methodref
    klass_info = frame.this_class.constant_pool[cp_item[1]]
    assert klass_info[0] == 7  # CONSTANT_Class_info
    name_and_type = frame.this_class.constant_pool[cp_item[2]]
    assert name_and_type[0] == 12  # name_and_type_index
    klass_name = frame.this_class.constant_pool[klass_info[1]][1]
    klass = frame.vm.get_class(klass_name)
    method_name = frame.this_class.constant_pool[name_and_type[1]][1]
    method_signature = frame.this_class.constant_pool[name_and_type[2]][1]
    method = klass.find_method(method_name, method_signature)

    logger.debug(klass_name)
    logger.debug(method_name)
    logger.debug(method_signature)
    logger.debug(frame.stack)

    if is_spec_lookup(frame.this_class, klass, method_name):
        method = None
        c = frame.this_class.super_class
        while method is None:
            if c is None:
                break
            if (method_name in c.methods and
                    method_signature in c.methods[method_name]):
                method = c.methods[method_name][method_signature]
                klass = c
                break
            c = c.super_class

    assert method is not None

    nargs = args_count(method_signature) + 1
    args = [None] * nargs
    while nargs > 0:
        value = frame.stack.pop()
        if type(value) is tuple and value[0] in ('long', 'double'):
            nargs -= 1
        args[nargs - 1] = value
        nargs -= 1

    assert len(args[0]) > 0
    jassert_ref(args[0])

    if args[0] is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return

    if method[0] & 0x0100 > 0:  # is native?
        exec_native(frame, args, klass, method_name, method_signature)
        return

    obj_mon = None
    if method[0] & 0x0020 > 0:  # is sync
        obj_mon = frame.vm.heap[args[0][1]]
        if "@monitor" in obj_mon.fields:
            if obj_mon.fields["@monitor"] == frame.thread:
                obj_mon.fields["@monitor_count"] += 1
            else:
                index = 0
                while index < len(args):
                    a = args[index]
                    if type(a) is tuple and a[0] in ('long', 'double'):
                        index += 1
                    else:
                        frame.stack.append(a)
                    index += 1
                raise SkipThreadCycle()
        else:
            obj_mon.fields["@monitor"] = frame.thread
            obj_mon.fields["@monitor_count"] = 1

    m_args = [''] * method[1]
    m_args[0:len(args)] = args[0:len(args)]

    instance = frame.vm.heap[args[0][1]]
    logger.debug("InvokeSpec: %s:%s %s", method_name, method_signature,
                 instance)
    sub = Frame(frame.thread, klass, method, m_args,
                "%s:%s %s" % (method_name, method_signature, instance))
    if obj_mon is not None:
        sub.monitor = obj_mon
    frame.thread.frame_stack.append(sub)


def is_spec_lookup(this_class, lookedup_class, method_name):
    if this_class.flags & 0x0020 == 0:
        return False
    if method_name == "<init>":
        return False
    if is_super_class(this_class, lookedup_class.this_name):
        return True
    else:
        return False


def is_super_class(this_class, super_name):
    if this_class.super_class is not None:
        if this_class.super_class.this_name == super_name:
            return True
        else:
            return is_super_class(this_class.super_class, super_name)
    return False
