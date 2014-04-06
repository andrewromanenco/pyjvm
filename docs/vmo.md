VM owned objects

There are few java objects which live outside of java heap and are handled by
pyjvm in a specific way (basically python code is called instead of java).

For example, STDOUT.
When you try to print something, your program usually uses System.out. This
gives you PrintStream object built around java.io.OutputStream instance.
In pyjvm this particular instance is owned by vm and has special reference:

> ("vm_ref", -1)

When vm receives order to call a method under such object, instead of real java
code, specific python function is called; for example when you print to 
System.out in background java tries to call:

> write(byte[] b, int off, int len)

So this call is translated to python:

> vmo1_write___BII_V(frame, args)

This code is in vmo.py and actually prints content of byte array to screen.


Another VM owned object is System Properties and it's is handled the same way.
See vmo.py for details.
This particular vmo object might be re-factored to all java (low priority).


When adding vm owned object, the crucial key is to make sure it's is the last
object in a chain to be called. This greatly reduces dev effort.
For example:
when one implements System.out there is option to make System.out to be owned by
vm. The problem is that type of out is PrintStream and all code of PrintStream
class has to be implemented in python. This is really useless coding as at the
end PrintStream calls an OutoutStream instance which has very simple interface.
Check java source code for PrintStream for details.