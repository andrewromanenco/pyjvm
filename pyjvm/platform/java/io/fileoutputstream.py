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


def java_io_FileOutputStream_initIDs___V(frame, args):
    # do nothing
    pass


def java_io_FileOutputStream_open__Ljava_lang_String_Z_V(frame, args):
    if args[1] is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    fis = frame.vm.heap[args[0][1]]
    ref = args[1]
    file_name = str_to_string(frame.vm, ref)
    append_flag = args[2]
    assert append_flag == 0, "File append is not yet here"
    if not os.path.isfile(file_name):
        frame.vm.raise_exception(frame, "java/io/FileNotFoundException")
        return
    size = os.path.getsize(file_name)
    f = open(file_name, 'wb')
    fis.fields["@file"] = f
    fis.fields["@available_bytes"] = size


def java_io_FileOutputStream_writeBytes___BIIZ_V(frame, args):
    if args[1] is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    fos = frame.vm.heap[args[0][1]]
    buf = frame.vm.heap[args[1][1]]
    offset = args[2]
    length = args[3]
    append_flag = args[4]
    assert append_flag == 0, "File append is not yet here"
    f = fos.fields["@file"]
    f.write(bytearray(buf.values[offset:length]))


def java_io_FileOutputStream_close0___V(frame, args):
    fos = frame.vm.heap[args[0][1]]
    f = fos.fields["@file"]
    f.close()
