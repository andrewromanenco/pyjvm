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
'''Java bytecode implementation'''

import logging

from pyjvm.bytecode import bytecode
from pyjvm.jassert import jassert_float
from pyjvm.jassert import jassert_double
from pyjvm.jassert import jassert_int
from pyjvm.jassert import jassert_long
from pyjvm.jassert import jassert_ref
from pyjvm.throw import JavaException

logger = logging.getLogger(__name__)


@bytecode(code=0xac)
def ireturn(frame):
    value = frame.stack.pop()
    logger.debug("To be returned {0}".format(value))
    jassert_int(value)
    frame.ret = value
    frame.has_result = True
    frame.pc = len(frame.code) + 1


@bytecode(code=0xad)
def lreturn(frame):
    value = frame.stack.pop()
    logger.debug("To be returned {0}".format(value))
    jassert_long(value)
    frame.ret = value
    frame.has_result = True
    frame.pc = len(frame.code) + 1


@bytecode(code=0xae)
def freturn(frame):
    value = frame.stack.pop()
    logger.debug("To be returned {0}".format(value))
    jassert_float(value)
    frame.ret = value
    frame.has_result = True
    frame.pc = len(frame.code) + 1


@bytecode(code=0xaf)
def dreturn(frame):
    value = frame.stack.pop()
    logger.debug("To be returned {0}".format(value))
    jassert_double(value)
    frame.ret = value
    frame.has_result = True
    frame.pc = len(frame.code) + 1


@bytecode(code=0xb0)
def areturn(frame):
    value = frame.stack.pop()
    jassert_ref(value)
    frame.ret = value
    frame.has_result = True
    frame.pc = len(frame.code) + 1


@bytecode(code=0xb1)
def return_(frame):
    frame.pc = len(frame.code) + 1


@bytecode(code=0xbf)
def athrow(frame):
    ref = frame.stack.pop()
    if ref is None:
        frame.vm.raise_exception(frame, "java/lang/NullPointerException")
        return
    jassert_ref(ref)
    frame.stack[:] = []  # empty stack
    frame.stack.append(ref)
    je = JavaException(frame.vm, ref)
    raise je
