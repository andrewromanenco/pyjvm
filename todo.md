PyJVM is very young project (as of April , 2014) and some features
are implemented just to make it work.
There is good chance items from this list will get higher priority.


sun.misc.Unsafe
 - Class should be reviewed
 - Under implemented

Exceptions do not have full stack trace
 - this will make debugging way easier

Wait/notify is not yest implemented
 - wait is already implemented
 - notify/notifyall is trivial, to be added with good use case

java.lang.Clazz
 - Minimal part is implemented just for for vm to startup

Review ops for right exceptions throwing
 - something might be missed
 - same for native methods implementations

Method synchronization
 - not supported for native methods - easy to add, not that easy to test

Double/Float
 - add normal support for double and float arithmetics
 - trivial with numpy, don't what to have this dependency
