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


def java_security_AccessController_getStackAccessControlContext___Ljava_security_AccessControlContext_(frame, args):
    frame.stack.append(None)


def java_security_AccessController_doPrivileged__Ljava_security_PrivilegedAction__Ljava_lang_Object_(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    klass = o.java_class
    method = klass.find_method("run", "()Ljava/lang/Object;")
    args = [None]*method[1]
    args[0] = ref
    sub = Frame(frame.thread, klass, method, args,
                "RUN call in java_security_AccessController_doPrivileged")
    frame.thread.frame_stack.append(sub)


def java_security_AccessController_doPrivileged__Ljava_security_PrivilegedExceptionAction__Ljava_lang_Object_(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    klass = o.java_class
    method = klass.find_method("run", "()Ljava/lang/Object;")
    assert method is not None
    args = [None]*method[1]
    args[0] = ref
    sub = Frame(frame.thread, klass, method, args,
                "RUN call in java_security_AccessController_doPrivileged")
    frame.thread.frame_stack.append(sub)
