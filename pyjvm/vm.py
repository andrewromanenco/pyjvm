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
'''Java Virtual Machine.
Initialization, threads, frame management.
'''

import logging
from collections import deque

from pyjvm.bytecode import get_operation
from pyjvm.class_loader import class_loader
from pyjvm.class_path import read_class_path
from pyjvm.frame import Frame
from pyjvm.jvmo import array_class_factory
from pyjvm.jvmo import JArray
from pyjvm.jvmo import JavaClass
from pyjvm.thread import Thread
from pyjvm.thread import SkipThreadCycle

from pyjvm.throw import JavaException

from pyjvm.vmo import VM_OBJECTS

from pyjvm.ops.ops_names import ops_name
from pyjvm.ops.ops_arrays import *
from pyjvm.ops.ops_calc import *
from pyjvm.ops.ops_cond import *
from pyjvm.ops.ops_convert import *
from pyjvm.ops.ops_fields import *
from pyjvm.ops.ops_invokespecial import *
from pyjvm.ops.ops_invokestatic import *
from pyjvm.ops.ops_invokevirtual import *
from pyjvm.ops.ops_invokeinterface import *
from pyjvm.ops.ops_misc import *
from pyjvm.ops.ops_ret import *
from pyjvm.ops.ops_setget import *
from pyjvm.ops.ops_shift import *

logger = logging.getLogger(__name__)


def vm_factory(class_path="."):
    '''Create JVM with specific class path'''
    return VM(class_path)


class VM(object):
    '''JVM implementation.
    See vm.txt in docs
    '''

    # Mark for vm caching
    serialization_id = 0
    initialized = False

    def __init__(self, _class_path="."):
        logger.debug("Creating VM")

        # Major memory structures
        self.perm_gen = {}
        self.heap = {}
        self.heap_next_id = 1
        #todo clean up self.cache_klass_klass = {}
        self.global_strings = {}

        # Handle for linked list of threads
        self.threads_queue = deque()
        self.non_daemons = 0

        self.top_group = None
        self.top_thread = None
        self.top_group_ref = None
        self.top_thread_ref = None

        self.class_path = read_class_path(_class_path)

        self.init_default_thread()

        # Load System and init major fields
        system_class = self.get_class("java/lang/System")

        # Set System.props to vm owned object
        system_class.static_fields["props"][1] = ("vm_ref",
                                                  VM_OBJECTS[
                                                      "System.Properties"])

        # STDout initialization using vm owned object
        ps_class = self.get_class("java/io/PrintStream")
        ps_object = ps_class.get_instance(self)
        ps_ref = self.add_to_heap(ps_object)
        method = ps_class.find_method("<init>", "(Ljava/io/OutputStream;)V")
        std_out_ref = ("vm_ref", VM_OBJECTS["Stdout.OutputStream"])
        thread = Thread(self, None)
        frame = Frame(thread, ps_class, method, [ps_ref, std_out_ref],
                      "PrintStream init")
        thread.frame_stack.append(frame)

        logger.debug("Run PrintStream init")
        self.run_thread(thread)  # Run exclusive thread
        system_class.static_fields["out"][1] = ps_ref

        system_class.static_fields["in"][1] = \
            ("vm_ref", VM_OBJECTS["Stdin.InputputStream"])

        # Additional parameters
        system_class.static_fields["lineSeparator"][1] = \
            self.make_heap_string("\n")

        # Load additional classes to speed up booting
        self.touch_classes()

        self.initialized = True

        logger.debug("VM created")

    def init_default_thread(self):
        '''Create initial thread group and thread.
        Both are java's objects
        '''
        tg_klass = self.get_class("java/lang/ThreadGroup")
        t_klass = self.get_class("java/lang/Thread")
        tg = tg_klass.get_instance(self)
        t = t_klass.get_instance(self)

        tg.fields["name"] = self.make_heap_string("system")
        tg.fields["maxPriority"] = 10
        t.fields["priority"] = 5
        t.fields["name"] = self.make_heap_string("system-main")
        t.fields["blockerLock"] = self.add_to_heap(
            self.get_class("java/lang/Object").get_instance(self))

        tg_ref = self.add_to_heap(tg)
        t_ref = self.add_to_heap(t)
        t.fields["group"] = tg_ref

        # Add thread to threadgroup; call byte code of void add(Thread)
        pvm_thread = Thread(self, t_ref)
        pvm_thread.is_alive = True
        method = tg_klass.find_method("add", "(Ljava/lang/Thread;)V")
        args = [None]*method[1]
        args[0] = tg_ref
        args[1] = t_ref
        frame = Frame(pvm_thread, tg_klass, method, args, "system tg init")
        pvm_thread.frame_stack.append(frame)
        self.run_thread(pvm_thread)

        self.top_group = tg
        self.top_thread = t
        self.top_group_ref = tg_ref
        self.top_thread_ref = t_ref

    def run_vm(self, main_klass, method, m_args):
        '''Run initialized vm with specific method of a class.
        This is class entered from command line. Method is looked up
        void main(String args[]).
        For more details see methods.txt in docs.
        '''
        t_klass = self.get_class("java/lang/Thread")
        t = t_klass.get_instance(self)
        t.fields["priority"] = 5
        t.fields["name"] = self.make_heap_string("main")
        t.fields["blockerLock"] = self.add_to_heap(
            self.get_class("java/lang/Object").get_instance(self))
        t_ref = self.add_to_heap(t)
        t.fields["group"] = self.top_group_ref

        pvm_thread = Thread(self, t_ref)
        pvm_thread.is_alive = True
        frame = Frame(pvm_thread, main_klass, method, m_args, "main")
        pvm_thread.frame_stack.append(frame)

        self.add_thread(pvm_thread)
        logger.debug("run thread pool")
        self.run_thread_pool()

    def get_class(self, class_name):
        '''Returns initialized class from pool (perm_gen) or loads
        it with class loader (and running static constructor).
        Getting a class might result in loading it's super first.
        '''
        if class_name is None:
            return  # this is look up for Object's super, which is  None
        if class_name in self.perm_gen:
            return self.perm_gen[class_name]
        if class_name[0] == '[':  # special treatment for arrays
            java_class = array_class_factory(self, class_name)
            lang_clazz = self.get_class("java/lang/Class")
            clazz_object = lang_clazz.get_instance(self)
            clazz_object.fields["@CLASS_NAME"] = class_name
            ref = self.add_to_heap(clazz_object)
            java_class.heap_ref = ref
            self.perm_gen[class_name] = java_class
            return java_class
        if class_name in ['byte', 'char', 'double', 'float', 'int', 'long',
                          'short', 'boolean']:
            java_class = JavaClass()
            self.perm_gen[class_name] = java_class
            java_class.is_primitive = True
            java_class.this_name = class_name
            lang_clazz = self.get_class("java/lang/Class")
            clazz_object = lang_clazz.get_instance(self)
            clazz_object.fields["@CLASS_NAME"] = class_name
            ref = self.add_to_heap(clazz_object)
            java_class.heap_ref = ref
            return java_class
        logger.debug("Class {0} not yet ready".format(class_name))
        java_class = class_loader(class_name, self.class_path)
        super_class = java_class.super_class
        if type(super_class) is unicode:  # lame check
            super_class = self.get_class(super_class)
            java_class.super_class = super_class
        logger.debug("Loaded class def\n{0}".format(java_class))
        self.perm_gen[class_name] = java_class
        # create actual java.lang.Class instance
        lang_clazz = self.get_class("java/lang/Class")
        clazz_object = lang_clazz.get_instance(self)
        clazz_object.fields["@CLASS_NAME"] = class_name
        ref = self.add_to_heap(clazz_object)
        java_class.heap_ref = ref
        self.run_static_constructor(java_class)
        return java_class

    def get_class_class(self, klass):
        '''Get class of class.
        Basically this is heap owned version of java.lang.Class
        '''
        return klass.heap_ref

    def run_static_constructor(self, java_class):
        '''Static constructor is run for every class loaded by class loader.
        It is executed in thread exclusive mode.
        '''
        logger.debug("Running static constructor for %s",
                     java_class.this_name)
        method = java_class.static_contructor()
        if method is None:
            logger.debug("No static constructor for %s",
                         java_class.this_name)
            return
        pvm_thread = Thread(self, self.top_thread_ref)
        pvm_thread.is_alive = True
        frame = Frame(pvm_thread, java_class, method, [None]*method[1],
                      "<clinit:{0}>".format(java_class.this_name))
        pvm_thread.frame_stack.append(frame)
        self.run_thread(pvm_thread)

        logger.debug("Finished with static constructor for %s",
                     java_class.this_name)

    def object_of_klass(self, o, klass_name):
        '''instanceOf implementation'''
        if o is None:
            return False
        if klass_name is None:
            return True
        klass = o.java_class
        while klass is not None:
            if klass_name == klass.this_name:
                return True
            klass = klass.super_class
        return False

    def add_to_heap(self, item):
        '''Put an item to java heap returning reference.
        Reference is in format ("ref", number)
        '''
        ref = self.heap_next_id
        self.heap[ref] = item
        self.heap_next_id += 1
        return ("ref", ref)

    def make_heap_string(self, value):
        '''Take python string and put java.lang.String instance to heap.
        String is represented by char array in background.
        Reference in heap is returned.
        Global caching is supported for all strings (same string always has
        same reference in heap)
        '''
        if value in self.global_strings:
            return self.global_strings[value]
        values = []
        for c in value:
            values.append(ord(c))
        array_class = self.get_class("[C")
        array = JArray(array_class, self)
        array.values = values
        arr_ref = self.add_to_heap(array)
        c = self.get_class("java/lang/String")
        o = c.get_instance(self)
        o.fields["value"] = arr_ref
        ref = self.add_to_heap(o)
        self.global_strings[value] = ref
        return ref

    def touch_classes(self):
        '''Touch some useful classes to speed up booting for cached vm'''
        self.get_class("java/lang/String")
        self.get_class("java/lang/Class")
        self.get_class("java/nio/CharBuffer")
        self.get_class("java/nio/HeapCharBuffer")
        self.get_class("java/nio/charset/CoderResult")
        self.get_class("java/nio/charset/CoderResult$1")
        self.get_class("java/nio/charset/CoderResult$Cache")
        self.get_class("java/nio/charset/CoderResult$2")

        thread_klass = self.get_class("java/lang/Thread")
        thread_klass.static_fields["MIN_PRIORITY"][1] = 1
        thread_klass.static_fields["NORM_PRIORITY"][1] = 5
        thread_klass.static_fields["MAX_PRIORITY"][1] = 10

    def add_thread(self, thread):
        '''Add py thread to pool'''
        self.threads_queue.append(thread)
        assert thread.java_thread is not None
        java_thread = self.heap[thread.java_thread[1]]
        if java_thread.fields["daemon"] == 0:
            self.non_daemons += 1

    def run_thread_pool(self):
        '''Run all threads.
        Threads are run one-by-one according to quota'''
        while len(self.threads_queue) > 0:
            thread = self.threads_queue.popleft()
            self.run_thread(thread, 100)
            if len(thread.frame_stack) == 0:
                thread.is_alive = False
                j_thread = self.heap[thread.java_thread[1]]
                assert j_thread is not None
                for o in j_thread.waiting_list:
                    o.is_notified = True
                java_thread = self.heap[thread.java_thread[1]]
                if java_thread.fields["daemon"] == 0:
                    self.non_daemons -= 1
                    if self.non_daemons == 0:
                        break
            else:
                self.threads_queue.append(thread)

    def run_thread(self, thread, quota=-1):
        '''Run single thread according to quota.
        Quota is number of byte codes to be executed.
        Quota -1 runs entire thread in exclusive mode.

        For each byte code specific operation function is called.
        Operation can throw exception.
        Thread may be busy (e.g. monitor is not available).
        Returns from syncronized methods are handled.
        '''
        frame_stack = thread.frame_stack
        while len(frame_stack) > 0:
            frame = frame_stack[-1]  # get current
            if frame.pc < len(frame.code):
                op = frame.code[frame.pc]
                frame.cpc = frame.pc
                frame.pc += 1
                # Make function name to be called
                op_call = hex(ord(op))

                #logger.debug("About to execute op_{2}: {0} ({3}) in {1}".format(
                #    op_call, frame.id, frame.pc - 1, ops_name[op_call]))
                
                opt = get_operation(op_call)
                if opt is None:
                    raise Exception("Op ({0}) is not yet supported".format(
                        op_call))
                try:
                    try:
                        opt(frame)
                        logger.debug("Stack:" + str(frame.stack))
                    except SkipThreadCycle:
                        # Thread is busy, call the same operation later
                        frame.pc = frame.cpc
                        break
                except JavaException as jexc:
                    # Exception handling
                    ref = jexc.ref
                    exc = self.heap[ref[1]]
                    handled = False
                    while not handled:
                        for (start_pc, end_pc, handler_pc, catch_type,
                             type_name) in frame.method[3]:
                            if start_pc <= frame.cpc < end_pc and \
                                    self.object_of_klass(exc, type_name):
                                frame.pc = handler_pc
                                frame.stack.append(ref)
                                handled = True
                                break
                        if handled:
                            break
                        frame_stack.pop()
                        if len(frame_stack) == 0:
                            raise
                        frame = frame_stack[-1]

            else:
                # Frame is done
                frame_stack.pop()
                if frame.monitor is not None:
                    assert frame.monitor.fields["@monitor"] == frame.thread
                    frame.monitor.fields["@monitor_count"] -= 1
                    if frame.monitor.fields["@monitor_count"] == 0:
                        del frame.monitor.fields["@monitor"]
                        del frame.monitor.fields["@monitor_count"]
                        frame.monitor = None
                # handle possible return VALUE
                if frame.has_result:
                    if len(frame_stack) > 0:
                        frame_stack[-1].stack.append(frame.ret)

            if quota != -1:
                quota -= 1
                if quota == 0:
                    break

    def raise_exception(self, frame, name):
        '''Util method to raise an exception based on name.
        e.g. java.lang.NullPointerException

        Exception is created on heap and throw op is called
        '''
        ex_klass = self.get_class(name)
        ex = ex_klass.get_instance(self)
        ref = self.add_to_heap(ex)

        method = ex_klass.find_method("<init>", "()V")
        m_args = [None]*method[1]
        m_args[0] = ref

        pvm_thread = Thread(self, None)
        pvm_thread.is_alive = True
        sub = Frame(pvm_thread, ex_klass, method, m_args, "exinit")
        pvm_thread.frame_stack.append(sub)
        self.run_thread(pvm_thread)

        frame.stack.append(ref)
        get_operation('0xbf')(frame)
