Class loading
=============

Class path is list of folders and jar files to read compiled java classes from.
Part of vm startup is creating memory structure for the class path.

The most important step is to locate rt.jar - this is major part of Java7
platform with all system classes (e.g. java.*; sun.*).

If jdk7 is installed and JAVA_HOME is set, pyjvm will try to locate rt.jar under
that location.
When no jdk exists, you should run get_rt.py in ./rt/ folder to download rt.jar
from my dropbox account (about 60 mb). This location (./rt/) is always checked
first and if rt.jar is found, then JAVA_HOME is ignored.

On the next step class path parameter (-cp) is read and parsed to jars and
folders. When this parameter is not submitted to pyjvm it's set to ".".

For each jar (including rt.jar) index of all files is created and is used to
actually load class file by name.

Class loader will use this cached index to lookup classes on their first use.
Order is:

 1. rt.jar content
 2. other jars
 3. folders from class path one by one
 4. fail app if not found

After class file is located it's is read and parsed to python representation.
Which is followed by static constructor execution.

Loading of a class triggers loading of superclass (up to java.lang.Object).

Class loader makes basic check to make sure class is compiled for Java7. Other
java versions are not supported and application will be closed.

The job of class loader is to read .class file and return JavaClass py object.

Custom class loaders are not supported (probably).
