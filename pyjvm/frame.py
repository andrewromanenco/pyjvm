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
'''Major execution component.

Created for every method execution and placed to thread's stack
'''

f_counter = 1  # make it easy to debug


class Frame(object):
    '''Frame is created for every method invocation'''

    def __init__(self, _thread, _this_class, _method, _args=[], _desc=""):
        self.thread = _thread
        if _thread is not None:
            self.vm = _thread.vm
        self.this_class = _this_class
        self.pc = 0  # Always points to byte code to be executed
        self.method = _method
        self.code = _method[2]  # method body (bytecode)
        self.stack = []
        self.args = _args
        self.ret = None  # return value for non void
        self.has_result = False  # flag if return value is set
        self.desc = _desc
        global f_counter
        self.id = f_counter
        # to support multithreaded environment
        self.cpc = 0
        self.monitor = None
        f_counter += 1
