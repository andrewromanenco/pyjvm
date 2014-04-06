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
'''Java related asserts'''

from pyjvm.jvmo import JArray


def jassert_float(value):
    assert type(value) is tuple and value[0] == "float"


def jassert_double(value):
    assert type(value) is tuple and value[0] == "double"


def jassert_int(value):
    assert type(value) is int or type(value) is long
    assert -2147483648 <= value <= 2147483647


def jassert_long(value):
    assert type(value) is tuple and value[0] == "long"
    assert -9223372036854775808 <= value[1] <= 9223372036854775807


def jassert_ref(ref):
    assert ref is None or (type(ref) is tuple and ref[0] in ("ref", "vm_ref"))


def jassert_array(array):
    assert array is None or isinstance(array, JArray)
