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


def sun_reflect_Reflection_getCallerClass___Ljava_lang_Class_(frame, args):
    caller_frame = frame.thread.frame_stack[
        len(frame.thread.frame_stack) - 2]
    klass = caller_frame.this_class
    ref = frame.vm.get_class_class(klass)
    frame.stack.append(ref)


def sun_reflect_Reflection_getClassAccessFlags__Ljava_lang_Class__I(frame, args):
    flag = 0x0001
    frame.stack.append(flag)
