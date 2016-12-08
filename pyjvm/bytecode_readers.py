# PyJVM (pyjvm.org) Java Virtual Machine implemented in pure Python
# Copyright (C) 2016 Andrew Romanenco (andrew@romanenco.com)
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
"""Various ways to read bytecode"""

import zipfile


def bytecode_from_file(file_path):
    '''Read bytecode from a file.'''
    with open(file_path, "rb") as bytecode:
        return bytecode.read()


def bytecode_from_jar(path_to_jar, class_name):
    '''Read bytecode from a jar. class_name is binary class name.'''
    archive = zipfile.ZipFile(path_to_jar, 'r')
    return archive.read(class_name + '.class')
