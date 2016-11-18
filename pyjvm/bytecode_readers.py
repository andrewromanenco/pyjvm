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
from abc import ABCMeta, abstractmethod

class AbstractBytecodeReader(metaclass=ABCMeta):
    """Provide read to a bytecode."""

    @abstractmethod
    def read(self, number_of_bytes):
        """Reads requested number of bytes and returns them as bytes."""
        pass

    @abstractmethod
    def size(self):
        """Returns total number of bytes. This is original data size."""
        pass


class BytecodeFileReader(AbstractBytecodeReader):
    '''Bytecode reader from a file.'''

    def __init__(self, file_path):
        '''Init with path to a file.'''
        self.pointer = 0
        with open(file_path, "rb") as bytecode:
            self.bytes = bytecode.read()

    def read(self, number_of_bytes):
        '''Read requested number of bytes and returns them instance of bytes'''
        result = self.bytes[self.pointer : (self.pointer + number_of_bytes)]
        self.pointer += number_of_bytes
        return result

    def size(self):
        '''Return total size of data.'''
        return len(self.bytes)

class JarBytecodeFileReader(BytecodeFileReader):
    '''Read bytecode from a file packed in a jar'''

    def __init__(self, path_to_jar, class_name):
        '''Init with a class identified by JVM class name from a given jar.'''
        self.pointer = 0
        archive = zipfile.ZipFile(path_to_jar, 'r')
        self.bytes = archive.read(class_name + '.class')
