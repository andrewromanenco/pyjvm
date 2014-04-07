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

import os

from pyjvm.utils import str_to_string


def java_io_FileInputStream_initIDs___V(frame, args):
    # do nothing
    pass


def java_io_FileInputStream_open__Ljava_lang_String__V(frame, args):
    if args[1] is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    fis = frame.vm.heap[args[0][1]]
    ref = args[1]
    file_name = str_to_string(frame.vm, ref)
    if not os.path.isfile(file_name):
        frame.vm.raise_exception(frame, "java/io/FileNotFoundException")
        return
    size = os.path.getsize(file_name)
    f = open(file_name, 'rb')
    fis.fields["@file"] = f
    fis.fields["@available_bytes"] = size


def java_io_FileInputStream_readBytes___BII_I(frame, args):
    fis = frame.vm.heap[args[0][1]]
    if fis.fields["@available_bytes"] == 0:
        frame.stack.append(-1)
        return
    buf = frame.vm.heap[args[1][1]]
    offset = args[2]
    length = args[3]
    f = fis.fields["@file"]
    data = f.read(length)
    for c in data:
        buf.values[offset] = ord(c)
        offset += 1
    fis.fields["@available_bytes"] -= len(data)
    frame.stack.append(int(len(data)))


def java_io_FileInputStream_available___I(frame, args):
    fis = frame.vm.heap[args[0][1]]
    if "@available_bytes" in fis.fields:
        frame.stack.append(fis.fields["@available_bytes"])
    else:
        frame.stack.append(0)


def java_io_FileInputStream_close0___V(frame, args):
    fis = frame.vm.heap[args[0][1]]
    f = fis.fields["@file"]
    f.close()
