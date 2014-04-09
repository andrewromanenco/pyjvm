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
"""pyjvm starting point

Run as 'python java.py -h' to get help info.
Most common use case:
    python java.py -cp CLASSPATH main.class.Name

JAVA_HOME must be set (in case you have jdk7 at you computer) or run
get_rt.py in rt folder to download dependencies.

See README.md for details
"""

import argparse
import logging
import os
import pickle

from pyjvm.class_path import read_class_path
from pyjvm.jvmo import JArray
from pyjvm.vm import vm_factory

SERIALIZATION_ID = 2  # inc for each VM init process update

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog='python pvm.py',
    description='Java Virtual Machine implemented in pure python')
parser.add_argument('-cp', nargs=1, default='.',
                    help='class path, jars and folders separated by semicolon')
parser.add_argument('-novmcache', dest='no_vm_cache',
                    action='store_const', const=True, default=False,
                    help='do not use vm caching(longer init time)')
parser.add_argument('clazz', nargs=1,
                    help='main class, e.g. some.package.MyClass')
parser.add_argument('param', nargs='*', help='argument for class')
program_args = parser.parse_args()


def main(args):
    '''Init VM and run requested java application'''
    logging.basicConfig(filename='pyjvm.log', filemode='w',
                        level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    main_class = args.clazz[0]
    class_path = args.cp[0]
    params = args.param
    use_vm_cache = not args.no_vm_cache

    vm = None
    if use_vm_cache:
        vm = load_cached_vm(SERIALIZATION_ID)
    if vm is None:
        vm = vm_factory(class_path)
        vm.serialization_id = SERIALIZATION_ID
        if use_vm_cache:
            cache_vm(vm)
    else:
        vm.class_path = read_class_path(class_path)

    # lookup starter class & main method
    class_name = main_class.replace(".", "/")
    logger.debug("Starting with class %s", str(class_name))
    java_class = vm.get_class(class_name)
    main_method = java_class.find_method("main", "([Ljava/lang/String;)V")

    if main_method is None:
        raise Exception("main method not found")

    logger.debug("Executing main")

    # create array of strings from command line parameters
    m_args = [''] * main_method[1]
    c_args = []
    for param in params:
        ref = vm.make_heap_string(param)
        c_args.append(ref)

    heap_array = ("refarr", "java/lang/String", c_args)
    ref_arr = vm.add_to_heap(heap_array)

    array_class = vm.get_class("[Ljava/lang/String;")
    heap_item = JArray(array_class, vm)
    heap_item.values = c_args
    ref = vm.add_to_heap(heap_item)
    m_args[0] = ref

    # run main
    vm.run_vm(java_class, main_method, m_args)

    logger.debug("*** VM DONE ***")


def load_cached_vm(serialization_id):
    '''Load from serialized file'''
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "vm-cache.bin")
    if os.path.isfile(path):
        cache_file = open(path, "r")
        vm = pickle.load(cache_file)
        cache_file.close()
        if hasattr(vm, 'serialization_id'):
            if vm.serialization_id == serialization_id:
                logger.debug("VM is loaded from cache")
                return vm
            else:
                logger.debug("Cached vm has different sid: %i",
                             vm.serialization_id)
        else:
            logger.debug("Cached vm has no sid")
    else:
        logger.debug("No cached vm file found")
    return None


def cache_vm(vm):
    '''Serialize vm to speed up startup time'''
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, "vm-cache.bin")
        cache_file = open(path, "w")
        pickle.dump(vm, cache_file)
        cache_file.close()
        logger.debug("VM cached with %i", vm.serialization_id)
    except Exception as exc:
        logger.error("Error caching vm: %s", str(exc))

if __name__ == '__main__':
    main(program_args)
