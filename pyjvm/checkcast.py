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
"""Major definitions for classes and instances"""

from pyjvm.prim import PRIMITIVES


def checkcast(s, t, vm):
    '''Check if a is instance of b
    both are classes from vm.get_class(...) - JavaClass
    '''
    if s.is_array:
        if t.is_array:
            s_name = s.this_name
            assert s_name[0] == '['
            t_name = t.this_name
            assert t_name[0] == '['
            s_name = s_name[1:]
            t_name = t_name[1:]
            if s_name[0] == 'L':
                s_name = s_name[1:-1]
            else:
                s_name = PRIMITIVES[s_name]
            if t_name[0] == 'L':
                t_name = t_name[1:-1]
            else:
                t_name = PRIMITIVES[t_name]
            sc = vm.get_class(s_name)
            tc = vm.get_class(t_name)
            if sc.is_primitive and tc.is_primitive:
                if sc == tc:
                    return True
                else:
                    return False
            return checkcast(sc, tc, vm)
        elif t.is_interface:
            for i in s.interfaces:
                if i == t.this_name:
                    return True
            return False
        else:
            if t.this_name == 'java/lang/Object':
                return True
            else:
                return False
    if s.is_interface:
        if t.is_interface:
            while s is not None:
                if t == s:
                    return True
                s = s.super_class
            return False
        if t.this_name == 'java/lang/Object':
            return True
        else:
            return False
    # S is object class
    if t.is_interface:
        while s is not None:
            for i in s.interfaces:
                i_c = vm.get_class(i)
                while i_c is not None:
                    if t == i_c:
                        return True
                    assert len(i_c.interfaces) < 2
                    if len(i_c.interfaces) == 1:
                        i_c = vm.get_class(i_c.interfaces[0])
                    else:
                        i_c = None
            s = s.super_class
        return False
    while s is not None:
        if t == s:
            return True
        s = s.super_class
    return False
