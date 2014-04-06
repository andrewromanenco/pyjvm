Threads
=======

Threads are represented by ThreadClass python objects. These py objects have
field java_thread - which is a reference to a java's instance of
java.lang.Thread in vm heap.

Thread has stack of frames. Frames are created for each method execution. See
jdk7 specification for details; pyjvm's frame is pretty close to original spec.

PyJVM has implementation of a multi-threaded system run on single core machine.
This means that actually all threads run in sequence one-by-one. Every thread
has running quota of 100 (this is hard-coded value).
Quota means the number of byte codes to be executed before putting current
thread on hold and executing next one.
Thread dies when there are no more steps to execute. Vm shutdowns when there
are no more non-daemon processes to run.

During a thread execution, thread my throw SkipThreadCycle exception. This will
force vm to switch to the next thread in the line, even if current thread still
has some unused quota. This may happen when thread can not proceed because of
synchronization block (monitor is busy). When this exception is caught, current
frame's pc (program counter) is reset to last executed op code and will be rerun
when the thread will be picked up for execution next time.


Synchronization
---------------

PyJVM supports synchronized blocks and methods (both static and instance).

Classes and instances have monitor and monitor_count fields to support locking.
Monitor has a link to a thread owning the lock. Monitor_count is supported for
multilevel locking; it is incremented when the same thread enters a guarded
code block and decremented when thread is out. When monitor_count gets back to
zero - monitor is unlocked.

For static synchronized methods see invokestatic.py.

For instance static methods and synchronized blocks see ops_invoke*.py and
ops_misc.py: monitorenter & monitorexit.

Handling for synchronized method exit is handled in vm.py: run_thread()

Wait&Notify are implemented in java.lang.Object class.