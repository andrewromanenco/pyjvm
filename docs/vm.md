PyJVM implementation
====================

Introduction
------------

PyJVM is python 2.7 based implementation of Java Virtual Machine 7.

It's loosely based on jdk7 specification (see oracle's web site). Most
exceptions are in runtime checks and binary compatibility. For example, if one's
try to call other's class private method - real jdk will throw an exception,
while pyjvm will execute it. Basically, java has both compile and run time,
and pyjvm has none - it's assuming that source of java classes is trusted.

PyJVM supports all byte code operations and has very few python coded shortcuts.

Project structure (under pyjvm):

 - ops: all java byte codes
 - platform: all native method calls (see natives.md)
 - *.py: see comments in those files


Types
-----

All java types are supported.

int, byte, short, char are plain python int.

float, double and long are tuples e.g. ("long", 123)

References - to instances in heap - are also tuples ("ref", 34). None for null.

VM owned objects: ("vm_ref", -1)

Classes are loaded with class loader from folders or jars and are represented by
JavaClass py object (also java.lang.Class instance may be created).


VM initialization
-----------------

For every fresh pyjvm instance there is an initialization process. This process
is responsible for loading all initial dependencies and creating system wide
objects - for example, initializing System.out. See vm.py init for details.

To speed up this phase vm caching is implemented. For every fresh start, after
vm is initialized and is about to run user application, file vm-cache.bin is
created with memory dump.

On every start, pyjvm checks if vm-cache.bin exists and if it's version matches
current code base. If it is - vm is loaded from the file.

There is constant: SERIALIZATION_ID in java.py - it should be incremented every
time when init process get changed. To reset caching for those users who has
old version already cached.

To ignore caching process pyjvm can be run with parameter: -novmcache


Memory structure
----------------

See vm.py

perm_gen - storage for py objects for java classes. Name based dictionary. When
code requests a specific class to get loaded this cache is always checked first.
There are no concept of class + classloader relation in pyjvm. Overall, this
should be refactored at some point.

heap - java heap. Number based dictionary; so a reference to an
object is ("ref", 4). Where number is the key. Heap contains only instance
fields, byte code itself (as well as static fields) is in perm_gen.


Garbage collection
------------------

See garbage_collector.md for details


Multi-threading
---------------

Multithreading and synchronization is supported. Based on "one-core" machine,
so all threads are executed in order based on small quota. See threads.md

Exceptions
----------

When java exception is about to be thrown - py instance of JavaException is
created. This JE instance has a filed - ref - which is a reference to actual
exception (e.g. java.lang.NullPointerException) object created in heap.
