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

from pyjvm.jassert import jassert_ref

logger = logging.getLogger(__name__)


def op_0xb2(frame):  # getstatic (a static field to stack)
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_fieldref = frame.this_class.constant_pool[index]
    assert cp_fieldref[0] == 9  # CONSTANT_Fieldref
    klass_info = frame.this_class.constant_pool[cp_fieldref[1]]
    assert klass_info[0] == 7  # CONSTANT_Class_info
    name_and_type = frame.this_class.constant_pool[cp_fieldref[2]]
    assert name_and_type[0] == 12  # CONSTANT_NameAndType_info
    klass_name = frame.this_class.constant_pool[klass_info[1]][1]
    field_name = frame.this_class.constant_pool[name_and_type[1]][1]

    logger.debug("getstatic %s %s", klass_name, field_name)
    klass = frame.vm.get_class(klass_name)

    while klass is not None and field_name not in klass.static_fields:
        klass = klass.super_class
    assert klass is not None

    value = klass.static_fields[field_name][1]
    frame.stack.append(value)


def op_0xb3(frame):  # putstatic (set a static field from stack)
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_fieldref = frame.this_class.constant_pool[index]
    assert cp_fieldref[0] == 9  # CONSTANT_Fieldref
    klass_info = frame.this_class.constant_pool[cp_fieldref[1]]
    assert klass_info[0] == 7  # CONSTANT_Class_info
    name_and_type = frame.this_class.constant_pool[cp_fieldref[2]]
    assert name_and_type[0] == 12  # CONSTANT_NameAndType_info
    klass_name = frame.this_class.constant_pool[klass_info[1]][1]
    field_name = frame.this_class.constant_pool[name_and_type[1]][1]

    logger.debug("putstatic %s %s", klass_name, field_name)
    klass = frame.vm.get_class(klass_name)

    while klass is not None and field_name not in klass.static_fields:
        klass = klass.super_class
    assert klass is not None

    value = frame.stack.pop()
    klass.static_fields[field_name][1] = value


def op_0xb4(frame):  # getfield (from an obj)
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_fieldref = frame.this_class.constant_pool[index]
    assert cp_fieldref[0] == 9  # CONSTANT_Fieldref
    klass_info = frame.this_class.constant_pool[cp_fieldref[1]]
    assert klass_info[0] == 7  # CONSTANT_Class_info
    name_and_type = frame.this_class.constant_pool[cp_fieldref[2]]
    assert name_and_type[0] == 12  # CONSTANT_NameAndType_info
    klass_name = frame.this_class.constant_pool[klass_info[1]][1]
    field_name = frame.this_class.constant_pool[name_and_type[1]][1]

    logger.debug("getfield %s %s", klass_name, field_name)
    klass = frame.vm.get_class(klass_name)
    # At some point make sure object has right class
    assert klass is not None

    ref = frame.stack.pop()
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)

    if ref[0] == "vm_ref":
        raise Exception("Special handling required, see vmo.txt")

    instance = frame.vm.heap[ref[1]]
    assert field_name in instance.fields
    frame.stack.append(instance.fields[field_name])


def op_0xb5(frame):  # putfield
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_fieldref = frame.this_class.constant_pool[index]
    assert cp_fieldref[0] == 9  # CONSTANT_Fieldref
    klass_info = frame.this_class.constant_pool[cp_fieldref[1]]
    assert klass_info[0] == 7  # CONSTANT_Class_info
    name_and_type = frame.this_class.constant_pool[cp_fieldref[2]]
    assert name_and_type[0] == 12  # CONSTANT_NameAndType_info
    klass_name = frame.this_class.constant_pool[klass_info[1]][1]
    field_name = frame.this_class.constant_pool[name_and_type[1]][1]

    logger.debug("putfield %s %s", field_name, klass_name)
    klass = frame.vm.get_class(klass_name)
    assert klass is not None

    value = frame.stack.pop()
    ref = frame.stack.pop()
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)

    if ref[0] == "vm_ref":
        raise Exception("Special handling required, see vmo.txt")

    instance = frame.vm.heap[ref[1]]
    assert field_name in instance.fields
    instance.fields[field_name] = value


def op_0xbb(frame):  # new
    index = (ord(frame.code[frame.pc]) << 8) + ord(frame.code[frame.pc + 1])
    frame.pc += 2
    cp_item = frame.this_class.constant_pool[index]
    assert cp_item[0] == 7  # CONSTANT_Class
    klass_name = frame.this_class.constant_pool[cp_item[1]][1]
    assert type(klass_name) is unicode
    klass = frame.vm.get_class(klass_name)  # make sure it is loaded

    instance = klass.get_instance(frame.vm)
    ref = frame.vm.add_to_heap(instance)
    frame.stack.append(ref)
