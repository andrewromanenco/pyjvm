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
from abc import ABCMeta

class AbstractBytecodeReader(metaclass=ABCMeta):
    """Provide read to a bytecode."""

    def __init__(self):
        '''Default constructor.'''
        self.bytes = None
        self.pointer = 0

    def read(self, number_of_bytes):
        '''Read requested number of bytes and returns them instance of bytes'''
        result = self.bytes[self.pointer : (self.pointer + number_of_bytes)]
        self.pointer += number_of_bytes
        return result

    def size(self):
        '''Return total size of data.'''
        return len(self.bytes)

class BytecodeFileReader(AbstractBytecodeReader):
    '''Bytecode reader from a file.'''

    def __init__(self, file_path):
        '''Init with path to a file.'''
        super().__init__()
        with open(file_path, "rb") as bytecode:
            self.bytes = bytecode.read()

class JarBytecodeFileReader(AbstractBytecodeReader):
    '''Read bytecode from a file packed in a jar'''

    def __init__(self, path_to_jar, class_name):
        '''Init with a class identified by JVM class name from a given jar.'''
        super().__init__()
        archive = zipfile.ZipFile(path_to_jar, 'r')
        self.bytes = archive.read(class_name + '.class')
