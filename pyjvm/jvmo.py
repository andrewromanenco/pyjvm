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

import logging

from pyjvm.prim import PRIMITIVES
from pyjvm.utils import default_for_type

logger = logging.getLogger(__name__)


class JavaClass(object):
    '''Java class representation inside python.
    Is loaded from .class by class loader
    '''

    def __init__(self):
        '''Init major components.
        See models.txt in docs.
        '''
        self.constant_pool = []
        # each field is name -> (desc, value)
        self.static_fields = {}
        # each field is name -> desc
        self.member_fields = {}
        self.methods = {}  # name-> desc-> (flags, nargs, code)
        self.interfaces = []  # names

        self.this_name = None
        self.super_class = None
        self.flags = 0
        self.is_interface = False
        self.is_primitive = False
        self.is_array = False

        # Reference to java.lang.Class
        self.heap_ref = None

    def print_constant_pool(self):
        '''Debug only purpose'''
        index = 0
        for record in self.constant_pool:
            print str(index) + ":\t" + str(record)
            index += 1

    def static_contructor(self):
        '''Find static constructor among class methods'''
        if "<clinit>" in self.methods:
            return self.methods["<clinit>"]["()V"]
        return None

    def find_method(self, name, signature):
        '''Find method by name and signature in current class or super'''
        if name in self.methods:
            if signature in self.methods[name]:
                return self.methods[name][signature]
        if self.super_class is not None:
            return self.super_class.find_method(name, signature)
        return None

    def get_instance(self, vm):
        '''Make class instance to be used in java heap'''
        logger.debug("Creating instance of " + str(self.this_name))
        return JavaObject(self, vm)

    def __str__(self):
        s = "JavaClass: "
        s += str(self.this_name) + "\n"
        if self.super_class is None:
            pass
        elif type(self.super_class) is unicode:
            s += "Super: *" + self.super_class + "\n"
        else:
            s += "Super: " + self.super_class.this_name + "\n"
        s += "Static fields: "
        for k in self.static_fields:
            s += "{0}{1} ".format(k, self.static_fields[k])
        s += "\n"
        s += "Member fields: "
        for k in self.member_fields:
            s += "{0}:{1} ".format(k, self.member_fields[k])
        s += "\n"
        s += "Methods:\n"
        for k in self.methods:
            s += "\t" + k + ": "
            for t in self.methods[k]:
                s += t + "::" + str(self.methods[k][t][1]) + ", "
            s += "\n"
        return s


class JavaObject(object):
    '''Java class instance.
    Piece of memory with all instance fields.
    Is created in heap.
    '''

    def __init__(self, jc, vm):
        self.java_class = jc
        self.fields = {}
        self.fill_fields(jc, vm)
        self.waiting_list = []  # wait/notify/notifyall

    def fill_fields(self, jc, vm):
        '''Init all fields with default values'''
        if jc is None:
            return
        for name in jc.member_fields:
            tp = jc.member_fields[name]
            if tp[0] == 'L':
                #vm.get_class(tp[1:-1])
                pass
            self.fields[name] = default_for_type(jc.member_fields[name])
        self.fill_fields(jc.super_class, vm)

    def __str__(self):
        return "Instance of {0}: {1}".format(self.java_class.this_name,
                                             self.fields)

    def __repr__(self):
        return self.__str__()


class JArray(object):
    '''Java array

    Lives in heap and has corresponding java_class
    '''
    def __init__(self, jc, vm):
        self.java_class = jc
        self.fields = {}
        self.values = []


def array_class_factory(vm, name):
    assert name[0] == '['
    name = name[1:]
    if name[0] == 'L':
        name = name[1:-1]
        vm.get_class(name)  # make sure it's in
        jc = JavaClass()
        jc.is_array = True
        jc.this_name = "[L" + name + ";"
        jc.super_class = vm.get_class("java/lang/Object")
        jc.interfaces = ["java/lang/Cloneable", "java/io/Serializable"]
        return jc
    if name[0] == '[':
        jc = JavaClass()
        jc.is_array = True
        jc.this_name = "[" + name
        jc.super_class = vm.get_class("java/lang/Object")
        jc.interfaces = ["java/lang/Cloneable", "java/io/Serializable"]
        return jc
    assert name in PRIMITIVES

    vm.get_class(PRIMITIVES[name])  # make sure class is in

    jc = JavaClass()
    jc.is_array = True
    jc.interfaces = ["java/lang/Cloneable", "java/io/Serializable"]
    jc.this_name = "[" + name
    jc.super_class = vm.get_class("java/lang/Object")
    return jc
