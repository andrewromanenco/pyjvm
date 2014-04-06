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
"""Test results checker

Read text file created as a result of test_runner.py run
"""

import sys

if len(sys.argv) < 2:
    print "Run as:"
    print "test_report.py <REPORT_FILE>"
    print
    print "REPORT_FILE is result of running:"
    print "test_runner.py > <REPORT_FILE>"
    print
    sys.exit()

report_file = sys.argv[1]
report = None
with open(report_file, 'r') as report:
    data = report.read()

assert data is not None

TARGET_SCORE = 8
SCORE = 0


def verify(value, test_name):
    global SCORE
    global data
    if value in data:
        print test_name,
        print "\tOK"
        SCORE += 1
    else:
        print "***",
        print test_name,
        print "\tFAIL"


verify("[ARRAYSTEST:36/36]", "bytecode.ArraysTest")
verify("[CALCSTEST:29/29]", "bytecode.CalcsTest")
verify("[HASHES:2/2]", "langfeatures.Hashes")
verify("[INNERCLAZZ:1/1]", "langfeatures.InnerClazz")
verify("From 1000 daemon 9", "langfeatures.ThreadsDaemons")
verify("first base: 109 =*10: 1090", "langfeatures.ThreadsSync")
verify("second base: -93 =*10: -930", "langfeatures.ThreadsSync")
verify("[1, 2, 3, 4, 5]", "sorts.HeapSort")

print
if SCORE == TARGET_SCORE:
    print "\t*** ALL TESTS ARE OK ***"
else:
    print "\t*** FAIL ***\t"
print
