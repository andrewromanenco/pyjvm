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

from pyjvm.frame import Frame
from pyjvm.thread import SkipThreadCycle
from pyjvm.thread import Thread


def java_lang_Thread_currentThread___Ljava_lang_Thread_(frame, args):
    ref = frame.thread.java_thread
    frame.stack.append(ref)


def java_lang_Thread_setPriority0__I_V(frame, args):
    pass  # just ignore


def java_lang_Thread_isAlive___Z(frame, args):
    ref = args[0]
    t = frame.vm.heap[ref[1]]
    if "@pvm_thread" in t.fields:
        if t.fields["@pvm_thread"].is_alive:
            frame.stack.append(1)
            return
    frame.stack.append(0)


def java_lang_Thread_start0___V(frame, args):
    '''Create new thread with one's void run()
    see thread.txt for details
    '''
    t_ref = args[0]
    o = frame.vm.heap[t_ref[1]]
    run = o.java_class.find_method("run", "()V")
    assert run is not None

    pvm_thread = Thread(frame.vm, t_ref)
    pvm_thread.is_alive = True
    m_args = [None] * run[1]
    m_args[0] = t_ref
    sub = Frame(pvm_thread, o.java_class, run, m_args, "Thread")
    pvm_thread.frame_stack.append(sub)
    frame.vm.add_thread(pvm_thread)


def java_lang_Thread_sleep__J_V(frame, args):
    '''Sleep until certain time'''
    if frame.thread.sleep_until == 0:
        now = int(time.time()) * 1000
        sleepMillis = args[0][1]
        threshold = now + sleepMillis
        frame.thread.sleep_until = threshold
        frame.pc -= 3  # no need !!!!!!!!!!!!!!!!!!!!!!!!!
        frame.stack.append(args[0])
        raise SkipThreadCycle()
    else:
        now = int(time.time()) * 1000
        if frame.thread.sleep_until > now:
            frame.pc -= 3  # no need !!!!!!!!!!!!!!!!!!!!!!!!!
            frame.stack.append(args[0])
            raise SkipThreadCycle()
        else:
            frame.thread.sleep_until = 0
            pass
