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
'''Java Exception'''


class JavaException(Exception):
    '''PY exception.

    Real heap reference is stored in ref
    '''

    def __init__(self, _vm, _ref):
        self.vm = _vm
        self.ref = _ref
        self.stack = []

    def __str__(self):
        ex = self.vm.heap[self.ref[1]]
        return str(ex)
