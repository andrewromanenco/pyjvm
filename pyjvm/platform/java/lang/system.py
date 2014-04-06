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

import time
import logging

from pyjvm.frame import Frame
from pyjvm.jassert import jassert_array
from pyjvm.thread import Thread

logger = logging.getLogger(__name__)


def java_lang_System_nanoTime___J(frame, args):
    nano = long(time.time()) * 1000
    logger.debug("System.nanoTime: " + str(nano))
    frame.stack.append(("long", nano))


def java_lang_System_currentTimeMillis___J(frame, args):
    currentTime = long(time.time()) * 1000
    logger.debug("System.currentTimeMillis: " + str(currentTime))
    frame.stack.append(("long", currentTime))


def java_lang_System_identityHashCode__Ljava_lang_Object__I(frame, args):
    ref = args[0]
    if ref is None:
        frame.stack.append(0)
        return
    assert type(ref) is tuple
    assert ref[0] == "ref"

    o = frame.vm.heap[ref[1]]
    klass = o.java_class
    method = klass.find_method("hashCode", "()I")

    if method[0] & 0x0100 > 0:
        # assuming native call to object's hashCode, get heap id
        frame.stack.append(ref[1])
        return

    pvm_thread = Thread(frame.vm, frame.vm.top_thread_ref)
    pvm_thread.is_alive = True
    m_args = [None]*method[1]
    m_args[0] = ref
    sub = Frame(pvm_thread, klass, method, m_args,
                "call get hashCode")
    pvm_thread.frame_stack.append(sub)
    frame.vm.run_thread(pvm_thread)
    assert sub.has_result
    frame.stack.append(sub.ret)


def java_lang_System_arraycopy__Ljava_lang_Object_ILjava_lang_Object_II_V(frame, args):
    #ref1, index1, ref2, index2, length
    count = args[4]
    index2 = args[3]
    ref2 = args[2]
    index1 = args[1]
    ref1 = args[0]
    assert type(count) is int
    assert type(index1) is int
    assert type(index2) is int
    assert type(ref1) is tuple and ref1[0] == "ref"
    assert type(ref2) is tuple and ref2[0] == "ref"
    arr1 = frame.vm.heap[ref1[1]]
    arr2 = frame.vm.heap[ref2[1]]
    jassert_array(arr1)
    jassert_array(arr2)
    # TODO NPE
    arr2.values[index2:index2 + count] = arr1.values[index1:index1 + count]
