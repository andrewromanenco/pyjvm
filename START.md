PyJVM - quick start
===================

 - you have some knowledge about java, compilation and class path settings
 - you have python 2.7 installed
 - latest version of pyjvm is downloaded from github
 - python is in your PATH

**With JAVA 7 installed:**
Set JAVA_HOME to actual jdk location

**Without JAVA 7:**
Go to ./rt/ folder in pyjvm and run get_rt.py.
This will download rt.jar of jdk 7 to ./rt/

To run actual java 7 compiled class
-----------------------------------
**See testcases folder for sample calls and java examples**

Assuming some.package.KlassName has static main method.

With standard java:

> java -cp some/class/path some.package.KlassName

PyJVM @ Windows:

> pava.cmd -cp some/class/path some.package.KlassName

PyJVM @ *nix/Mac:

> ./pava -cp some/class/path some.package.KlassName

*Assuming pava/pava.cmd is in your PATH - you can just replace java with
pava to run your application.*

Class path
----------
Class path is configured with -cp parameter and default value is set to current
folder ("."). To add other folders and/or jar files use -cp with list of those
folders and jars separated by ":".

Use cases
---------
**Run** class MyClass which is in default package and is in current
folder (MyClass.class file exists):

> ./pava MyClass

or

> ./pava -cp . MyClass

**Run** class in MyClass from package abc.de, assuming MyClass.class
is in ./abc/de/

> ./pava abc.de.MyClass

**Run** class in MyClass from package abc.de, class is in jar Some.jar

> ./pava -jar Some.jar abc.de.MyClass


Troubleshooting
---------------

There is good chance that your application will call native java method not yet
implemented in python. In this case you will get error message similar to:

> Exception: Op (SOME_NAME_HERE) is not yet supported in natives

Unfortunately you have only two options: wait or implement it yourself. See
documentation for more details (natives.txt and developers.txt)

Other types of errors probably should be reported, including log file (created
in pyjvm folder) and sample java source code.