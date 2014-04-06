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
'''JMV threads'''


class Thread(object):
    '''JMV thread.
    See threads.txt in documentation for details.
    '''

    def __init__(self, _vm, _java_thread):
        '''Init pyjvm thread
        _vm reference to current vm
        _java_thread reference to java's Thread instance in heap
        '''
        # One frame per method invocation
        self.frame_stack = []
        self.vm = _vm
        # Support looping for multi-threaded apps
        self.next_thread = None
        self.prev_thread = None
        # Reference to java's Thread instances
        self.java_thread = _java_thread
        self.is_alive = False
        self.waiting_notify = False
        self.is_notified = False
        self.monitor_count_cache = 0
        # For sleep(long) support
        self.sleep_until = 0
        if _java_thread is not None:
            obj = _vm.heap[_java_thread[1]]
            obj.fields["@pvm_thread"] = self


class SkipThreadCycle(Exception):
    '''Thread may skip his execution quota in case when a monitor
    is busy or sleep was called
    '''
    pass
