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

from pyjvm.frame import Frame
from pyjvm.thread import Thread
from pyjvm.utils import str_to_string


def sun_reflect_NativeConstructorAccessorImpl_newInstance0__Ljava_lang_reflect_Constructor__Ljava_lang_Object__Ljava_lang_Object_(frame, args):
    '''Create instance of a class, with constructor call'''
    ref = args[0]
    params = args[1]
    assert type(ref) is tuple and ref[0] == "ref"
    assert params is None or len(params) == 0
    o = frame.vm.heap[ref[1]]
    klass_klass = frame.vm.heap[o.fields["clazz"][1]]
    clazz = frame.vm.get_class(klass_klass.fields["@CLASS_NAME"])
    signature = str_to_string(frame.vm, o.fields["signature"])
    assert signature == "()V"
    instance = clazz.get_instance(frame.vm)
    iref = frame.vm.add_to_heap(instance)
    frame.stack.append(iref)
    method = clazz.find_method("<init>", signature)

    # actully running constructor in exclusive mode
    pvm_thread = Thread(frame.vm, frame.vm.top_thread_ref)
    pvm_thread.is_alive = True
    m_args = [None]*method[1]
    m_args[0] = iref
    sub = Frame(pvm_thread, clazz, method, m_args, "nativ instance0")
    pvm_thread.frame_stack.append(sub)
    frame.vm.run_thread(pvm_thread)
