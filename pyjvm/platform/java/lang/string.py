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

from pyjvm.utils import arr_to_string


def java_lang_String_intern___Ljava_lang_String_(frame, args):
    ref = args[0]
    assert type(ref) is tuple and ref[0] == "ref"
    o = frame.vm.heap[ref[1]]
    ref = o.fields["value"]
    o = frame.vm.heap[ref[1]]  # this is JArray
    s = arr_to_string(o.values)
    ref = frame.vm.make_heap_string(s)
    frame.stack.append(ref)
