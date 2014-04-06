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
"""VMO Virtual Machine owned objects.
These are instances of java classes handled by VM code instead of byte
code. These objects do not reside in heap. Their reference is
("vm_ref", x), where x < 0; versus normal heap owned objects:
("ref", y), y > 0
When a method is called on these vm owned instances, python code is
executed. This is different from handling native methods.

Example of vm owned object is STDOUT (print something on the screen).
"""

import logging
import sys

from pyjvm.jassert import jassert_array
from pyjvm.utils import str_to_string

logger = logging.getLogger(__name__)

VM_OBJECTS = {
    "Stdout.OutputStream": -1,
    "System.Properties": -2,
    "JavaLangAccess": -3,
    "Stdin.InputputStream": -4
    }

VM_CLASS_NAMES = {
    -1: "java/io/OutputStream",
    -2: "java/util/Properties",
    -3: "sun/misc/JavaLangAccess",
    -4: "java/io/InputStream"
}


def vm_obj_call(frame, args, method_name, method_signature):
    '''Called by invoke method operations when instance ref is ("vm_ref", x).
    This methods converts call to function name defined in this file. It is
    executed (python code) instead of original byte code.
    '''
    ref = args[0]
    assert type(ref) is tuple
    assert ref[0] == "vm_ref"
    assert ref[1] < 0
    logger.debug("VM owned obj call: %s", ref[1])
    lookup_name = "vmo%s_%s_%s" % (ref[1] * -1, method_name, method_signature)
    lookup_name = lookup_name.replace("/", "_")
    lookup_name = lookup_name.replace("(", "_")
    lookup_name = lookup_name.replace(")", "_")
    lookup_name = lookup_name.replace("[", "_")
    lookup_name = lookup_name.replace(";", "_")
    lookup_name = lookup_name.replace(".", "_")
    if lookup_name not in globals():
        logger.error("VMOcall not implemented: %s:%s for %d", method_name,
                     method_signature, ref[1])
        raise Exception("Op ({0}) is not yet supported in vmo".format(
            lookup_name))
    globals()[lookup_name](frame, args)


def vmo_check_cast(vm, vmo_id, klass):
    '''check cast for specific vmo object

    vmo_id is less than zero, klass is JavaClass
    True if vmo is subclass of klass or implements interface klass
    '''
    this_klass = VM_CLASS_NAMES[vmo_id]
    klass_name = klass.this_name
    while klass is not None:
        if klass.this_name == this_klass:
            return True
        else:
            klass = klass.super_class
    vmo_klass = vm.get_class(this_klass)
    for i in vmo_klass.interfaces:
        if i == klass_name:
            return True
    return False


def vmo1_write___BII_V(frame, args):
    '''java.io.OutputStream
    void write(byte[] b, int off, int len)
    '''
    buf = args[1]
    offset = args[2]
    length = args[3]
    arr = frame.vm.heap[buf[1]]
    jassert_array(arr)
    chars = arr.values
    for index in range(offset, offset + length):
        sys.stdout.write(chr(chars[index]))


def vmo2_getProperty__Ljava_lang_String__Ljava_lang_String_(frame, args):
    '''java.lang.System
    public static String getProperty(String key)
    This is call to java.util.Properties object
    '''
    s_ref = args[1]
    value = str_to_string(frame.vm, s_ref)
    # refactor this code someday
    # ok for now, as all refs are cached
    props = {}
    props["file.encoding"] = frame.vm.make_heap_string("utf8")
    props["line.separator"] = frame.vm.make_heap_string("\n")
    if value in props:
        ref = props[value]
        assert type(ref) is tuple and ref[0] == "ref"
        frame.stack.append(ref)
        return
    frame.stack.append(None)


def vmo4_read___BII_I(frame, args):
    '''In will be truncated at 8k'''
    # TODO all exception checks
    ref = args[1]
    offset = args[2]
    length = args[3]
    o = frame.vm.heap[ref[1]]
    array = o.values

    c = sys.stdin.read(1)
    if c == '':
        frame.stack.append(-1)
    array[offset] = ord(c)
    if ord(c) == 10:
        frame.stack.append(1)
        return
    i = 1
    while i < length:
        c = sys.stdin.read(1)
        if c == '':
            break
        array[offset + i] = ord(c)
        i += 1
        if ord(c) == 10:
            break
    frame.stack.append(i)


def vmo4_available___I(frame, args):
    '''This is always zero. No support for buffering'''
    frame.stack.append(0)


def vmo4_read___I(frame, args):
    '''Read single byte'''
    c = sys.stdin.read(1)
    if c == '':
        frame.stack.append(-1)
    else:
        frame.stack.append(ord(c))
