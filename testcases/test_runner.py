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
"""Run pyjvm test cases

    test_runnet.py > output.txt

then use test_report.py to verify results

Test runner creates VM instance in memory. For every test case VM is cloned.
Test cases are regular java classes, compiled for java 7.
"""

import copy
import logging
import os
import platform
import sys

logging.disable(logging.INFO)

sys.path.append('../.')

from pyjvm.vm import vm_factory

print
print "PyVJM test runner"
print

print "System information:"
print platform.platform()
print platform.version()
print

JAVA_HOME = os.environ.get('JAVA_HOME')
LOCAL_RT = os.path.isfile('../rt/rt.jar')
if JAVA_HOME is None and not LOCAL_RT:
    print "*** CAN NOT RUN TESTS ***"
    print "Set JAVA_HOME or init rt: see START.md for details"
    sys.exit()
print "Initializing Java Virtual Machine"
vm = vm_factory('../testcases/bin/')
print "VM is initialized"


def run(vm, klass_name):
    klass_name = klass_name.replace(".", "/")
    klass = vm.get_class(klass_name)
    main_method = klass.find_method("main", "([Ljava/lang/String;)V")
    m_args = [''] * main_method[1]
    vm.run_vm(klass, main_method, m_args)


print "TestCase1.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "bytecode.CalcsTest")
print "TestCase1.End"
print

print "TestCase2.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "bytecode.ArraysTest")
print "TestCase2.End"
print

print "TestCase3.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "langfeatures.Hashes")
print "TestCase3.End"
print

print "TestCase4.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "langfeatures.InnerClazz")
print "TestCase4.End"
print

print "TestCase5.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "langfeatures.PrintOut")
print "TestCase5.End"
print

print "TestCase6.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "langfeatures.ThreadsDaemons")
print "TestCase6.End"
print

print "TestCase7.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "langfeatures.ThreadsSync")
print "TestCase7.End"
print

print "TestCase8.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "sorts.HeapSort")
print "TestCase8.End"
print

print "TestCase9.Begin"
testcase = copy.deepcopy(vm)
run(testcase, "io.FilePrint")
print "TestCase9.End"
print

