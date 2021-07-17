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
"""Common utils"""


def arr_to_string(str_arr):
    '''Convert string's array to real unicode string'''
    result_string = ""
    for char_ in str_arr:
        result_string += str(unichr(char_))
    return result_string


def str_to_string(vm, ref):
    '''Convert java string reference to unicode'''
    if ref is None:
        return "NULL"
    heap_string = vm.heap[ref[1]]
    value_ref = heap_string.fields["value"]
    value = vm.heap[value_ref[1]]  # this is array of chars
    return arr_to_string(value.values)


def args_count(desc):
    '''Get arguments count from method signature string
    e.g. ()V - 0; (II)V - 2 (two int params)
    '''
    count = _args_count(desc[1:])
    return count


def _args_count(desc):
    '''Recursive parsing for method signature'''
    char_ = desc[0]
    if char_ == ")":
        return 0
    if char_ in ["B", "C", "F", "I", "S", "Z"]:
        return 1 + _args_count(desc[1:])
    if char_ in ["J", "D"]:
        return 2 + _args_count(desc[1:])
    if char_ == "L":
        return 1 + _args_count(desc[desc.index(";") + 1:])
    if char_ == "[":
        return _args_count(desc[1:])
    raise Exception("Unknown type def %s", str(char_))


def default_for_type(desc):
    '''Get default value for specific type'''
    if desc == "I":
        return 0
    elif desc == "J":  # long
        return ("long", 0)
    elif desc[0] == "[":  # array
        return None
    elif desc[0] == 'L':  # object
        return None
    elif desc == 'Z':  # boolean
        return 0
    elif desc == 'D':  # double
        return ("double", 0.0)
    elif desc == 'F':  # float
        return ("float", 0.0)
    elif desc == 'C':  # char
        return 0
    elif desc == 'B':  # boolean
        return 0
    raise Exception("Default value not yet supported for " + desc)


def category_type(value):
    '''Get category type of a variable according to jdk specs

    long, double are 2, others are 1'''
    if type(value) is tuple and value[0] in ('long', 'double'):
        return 2
    else:
        return 1
