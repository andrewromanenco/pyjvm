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
'''Natives methods handler '''

import logging

import re
from pyjvm.platform.java.lang.clazz import *
from pyjvm.platform.java.lang.double import *
from pyjvm.platform.java.lang.float import *
from pyjvm.platform.java.lang.object import *
from pyjvm.platform.java.lang.runtime import *
from pyjvm.platform.java.lang.string import *
from pyjvm.platform.java.lang.system import *
from pyjvm.platform.java.lang.thread import *
from pyjvm.platform.java.lang.throwable import *
from pyjvm.platform.java.io.filesystem import *
from pyjvm.platform.java.security.accesscontroller import *
from pyjvm.platform.sun.misc.unsafe import *
from pyjvm.platform.sun.misc.vm import *
from pyjvm.platform.sun.reflect.nativeconstructoraccessorimpl import *
from pyjvm.platform.sun.reflect.reflection import *

logger = logging.getLogger(__name__)

LOOKUP_REPLACEMENT = re.compile(r"[-\.\;/()\[]")

def exec_native(frame, args, klass, method_name, method_signature):
    '''Handle calls to java's native methods.
    Create function name from class and method names and call that
    implementation.
    See native.txt in documentation.
    '''
    if method_name == "registerNatives" and method_signature == "()V":
        logger.debug("No need to call native registerNatives()V for class: %s",
                     klass.this_name)
        return
    
    lookup_name = "_".join([klass.this_name, method_name, method_signature])
    lookup_name = re.sub(LOOKUP_REPLACEMENT, "_", lookup_name)

    if lookup_name not in globals():
        logger.error("Native not yet ready: %s:%s in %s", method_name,
                     method_signature, klass.this_name)
        raise Exception("Op ({0}) is not yet supported in natives".format(
                        lookup_name))
    globals()[lookup_name](frame, args)
