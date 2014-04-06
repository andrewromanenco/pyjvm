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
'''See natives.txt in documentation'''

#
# NOT FULLY IMPLEMENTED!!!!
# JUST ENOUGHT TO MAKE IT WORK
#
# Constructor paremeters always empty
#

import logging

from pyjvm.jvmo import JArray
from pyjvm.jvmo import JavaClass
from pyjvm.utils import arr_to_string, str_to_string

from pyjvm.ops.ops_cond import checkcast

logger = logging.getLogger(__name__)


def java_lang_Class_getName0___Ljava_lang_String_(frame, args):
    ref = args[0]
    assert type(ref) is tuple
    klass_klass = frame.vm.heap[ref[1]]
    klass_name = klass_klass.fields["@CLASS_NAME"]
    assert klass_name is not None
    klass_name = klass_name.replace("/", ".")
    result = frame.vm.make_heap_string(klass_name)
    frame.stack.append(result)


def java_lang_Class_getClassLoader0___Ljava_lang_ClassLoader_(frame, args):
    ref = args[0]
    assert type(ref) is tuple
    frame.stack.append(None)  # always bootstrap


def java_lang_Class_desiredAssertionStatus0__Ljava_lang_Class__Z(frame, args):
    frame.stack.append(0)


def java_lang_Class_getPrimitiveClass__Ljava_lang_String__Ljava_lang_Class_(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    instance = frame.vm.heap[ref[1]]
    assert instance.java_class.this_name == "java/lang/String"
    value_ref = instance.fields["value"]
    value = arr_to_string(frame.vm.heap[value_ref[1]].values)
    jc = frame.vm.get_class(value)
    frame.stack.append(jc.heap_ref)


def java_lang_Class_isInterface___Z(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    klass_name = o.fields["@CLASS_NAME"]
    klass = frame.vm.get_class(klass_name)
    if klass.is_interface:
        frame.stack.append(1)
    else:
        frame.stack.append(0)


def java_lang_Class_isPrimitive___Z(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    klass_name = o.fields["@CLASS_NAME"]
    klass = frame.vm.get_class(klass_name)
    if klass.is_primitive:
        frame.stack.append(1)
    else:
        frame.stack.append(0)


def java_lang_Class_getModifiers___I(frame, args):
    flag = 0x0001
    frame.stack.append(flag)


def java_lang_Class_getSuperclass___Ljava_lang_Class_(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    klass_name = o.fields["@CLASS_NAME"]
    klass = frame.vm.get_class(klass_name)
    if klass.this_name == "java/lang/Object":
        frame.stack.append(None)
        return
    s_klass = klass.super_class
    frame.stack.append(s_klass.heap_ref)


def java_lang_Class_getDeclaredConstructors0__Z__Ljava_lang_reflect_Constructor_(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    klass_name = o.fields["@CLASS_NAME"]
    klass = frame.vm.get_class(klass_name)
    c_klass = frame.vm.get_class("java/lang/reflect/Constructor")
    cons = []

    if "<init>" in klass.methods:
        for m in klass.methods["<init>"]:
            c = c_klass.get_instance(frame.vm)
            c.fields["clazz"] = klass.heap_ref
            sign_ref = frame.vm.make_heap_string(m)
            c.fields["signature"] = sign_ref
            cref = frame.vm.add_to_heap(c)
            array_class = frame.vm.get_class("[Ljava/lang/Class;")
            params = JArray(array_class, frame.vm)
            params_ref = frame.vm.add_to_heap(params)
            c.fields["parameterTypes"] = params_ref
            cons.append(cref)
    array_class = frame.vm.get_class("[Ljava/lang/reflect/Constructor;")
    heap_item = JArray(array_class, frame.vm)
    heap_item.values = cons
    ref = frame.vm.add_to_heap(heap_item)
    frame.stack.append(ref)


def java_lang_Class_isArray___Z(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    klass_name = o.fields["@CLASS_NAME"]
    klass = frame.vm.get_class(klass_name)
    if klass.is_array:
        frame.stack.append(1)
    else:
        frame.stack.append(0)


def java_lang_Class_forName0__Ljava_lang_String_ZLjava_lang_ClassLoader__Ljava_lang_Class_(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    name = str_to_string(frame.vm, ref)
    name = name.replace(".", "/")
    klass = frame.vm.get_class(name)
    ref = frame.vm.get_class_class(klass)
    frame.stack.append(ref)


def java_lang_Class_getDeclaredFields0__Z__Ljava_lang_reflect_Field_(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    klass_name = o.fields["@CLASS_NAME"]
    klass = frame.vm.get_class(klass_name)
    field_klass = frame.vm.get_class("java/lang/reflect/Field")
    fields = []
    for field_name in klass.member_fields:
        field = field_klass.get_instance(frame.vm)
        name_ref = frame.vm.make_heap_string(field_name)
        field.fields["name"] = name_ref
        field.fields["clazz"] = klass.heap_ref
        field._name = field_name
        fref = frame.vm.add_to_heap(field)
        fields.append(fref)
    array_class = frame.vm.get_class("[Ljava/lang/reflect/Field;")
    heap_item = JArray(array_class, frame.vm)
    heap_item.values = fields
    ref = frame.vm.add_to_heap(heap_item)
    frame.stack.append(ref)


def java_lang_Class_isAssignableFrom__Ljava_lang_Class__Z(frame, args):
    # TODO NPE
    ref_o = args[0]
    ref_x = args[1]
    o = frame.vm.heap[ref_o[1]]
    o_klass = frame.vm.get_class(o.fields["@CLASS_NAME"])
    x = frame.vm.heap[ref_x[1]]
    x_klass = frame.vm.get_class(x.fields["@CLASS_NAME"])
    if checkcast(x_klass, o_klass, frame.vm):
        frame.stack.append(1)
    else:
        frame.stack.append(0)
