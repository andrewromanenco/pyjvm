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

import struct


def java_lang_Double_doubleToRawLongBits__D_J(frame, args):
    value = args[0]
    assert type(value) is tuple
    assert value[0] == "double"
    packed = struct.pack('>d', value[1])
    packed = struct.unpack('>q', packed)[0]  # IEEE 754 floating-point
    frame.stack.append(("long", packed))


def java_lang_Double_longBitsToDouble__J_D(frame, args):
    value = args[0]
    assert type(value) is tuple
    assert value[0] == "long"
    packed = struct.pack('>q', value[1])
    packed = struct.unpack('>d', packed)[0]  # IEEE 754 floating-point
    frame.stack.append(("double", packed))
