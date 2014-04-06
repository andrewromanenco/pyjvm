Garbage collector
=================

Java is known for moving memory management responsibilities from a developer to
JVM. At this moment **NO garbage collector is implemented** in pyjvm.

Before actually adding one, abstract api should be added to eliminate hard
coded logic. This work is in progress.

After API is done, these options might be implemented:

 - Collectors described in JMV 7 specs
 - Reference counting collector
 