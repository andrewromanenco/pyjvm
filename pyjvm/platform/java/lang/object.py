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

from pyjvm.jvmo import JArray
from pyjvm.thread import SkipThreadCycle


def java_lang_Object_getClass___Ljava_lang_Class_(frame, args):
    assert len(args) > 0
    assert type(args[0]) is tuple
    assert args[0][0] == "ref" and args[0][1] > 0
    o = frame.vm.heap[args[0][1]]
    klass = o.java_class
    ref = frame.vm.get_class_class(klass)
    frame.stack.append(ref)


def java_lang_Object_hashCode___I(frame, args):
    assert type(args[0]) is tuple
    frame.stack.append(args[0][1])  # address in heap is object's hash


def java_lang_Object_wait__J_V(frame, args):
    ref = args[0]
    waiting_time = args[1]
    assert ref is not None
    # NPE
    o = frame.vm.heap[ref[1]]
    assert o is not None
    t = frame.thread

    if t.is_notified:
        t.waiting_notify = False
        if "@monitor" in o.fields:
            frame.stack.append(ref)
            frame.stack.append(waiting_time)
            raise SkipThreadCycle()
        else:
            o.waiting_list.remove(t)
            o.fields["@monitor"] = t
            o.fields["@monitor_count"] = t.monitor_count_cache
            t.is_notified = False
            return

    if t.waiting_notify:
        if t.sleep_until > 0:
            now = int(time.time()) * 1000
            if now <= t.sleep_until:
                if "@monitor" in o.fields:
                    frame.stack.append(ref)
                    frame.stack.append(waiting_time)
                    raise SkipThreadCycle()
                else:
                    o.waiting_list.remove(t)
                    o.fields["@monitor"] = t
                    o.fields["@monitor_count"] = t.monitor_count_cache
                    t.is_notified = False
                    t.waiting_notify = False
                    return
        frame.stack.append(ref)
        frame.stack.append(waiting_time)
        raise SkipThreadCycle()
    else:
        assert "@monitor" in o.fields
        assert o.fields["@monitor"] == frame.thread
        o.waiting_list.append(t)
        t.waiting_notify = True
        if waiting_time[1] > 0:
            now = int(time.time()) * 1000
            t.sleep_until = now + waiting_time[1]
        t.monitor_count_cache = o.fields["@monitor_count"]
        del o.fields["@monitor"]
        del o.fields["@monitor_count"]
        frame.stack.append(ref)
        frame.stack.append(waiting_time)
        raise SkipThreadCycle()


def java_lang_Object_clone___Ljava_lang_Object_(frame, args):
    # TODO NPE
    o = frame.vm.heap[args[0][1]]
    if o.java_class.is_array:
        clone = JArray(o.java_class, frame.vm)
        clone.values = o.values[:]
        ref = frame.vm.add_to_heap(clone)
        frame.stack.append(ref)
    else:
        clone = o.java_class.get_instance(frame.vm)
        clone.fields = o.fields.copy()
        ref = frame.vm.add_to_heap(clone)
        frame.stack.append(ref)
