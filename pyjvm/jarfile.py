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
'''Module to work with JAR files'''

import atexit
import zipfile

_opened = {}

def jar(jarfile):
    """Open JAR file as zip or return already opened file"""
    if not zipfile.is_zipfile(jarfile):
        raise AssertionError("%(jarfile)s is not a valid JAR." % locals())

    return _opened.setdefault(jarfile, _opened.get(jarfile) or zipfile.ZipFile(jarfile, 'r'))


def get_content(jarfile, predicat):
    """Returns list of .class files from jar file

    @param jarfile: filepath to jarfile
    @param predicat: predicat function
    @return: list of files inside jar satisfying a predicate
    """
    j = jar(jarfile)
    return [name for name in j.namelist() if predicat(name)]


def _close_files():
    """Close opened files"""
    for zip in _opened.values():
        zip.close()

atexit.register(_close_files)
