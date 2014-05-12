Here is step by step JMV extension to support unimplemented native methods.

See commit: 0d3807e80e9a2a79edd40f6d3e6170ab91875334

Use case java code: testcases/src/io/FileExists.java
Program reads file name from arguments and checks if the file exists.

After running this sample app with pyjvm, this exception is printed:

Exception: Op (java_io_FileSystem_getFileSystem___Ljava_io_FileSystem_) is not yet supported in natives

Basically this means that an implementation is missing:

Class: java.io.FileSystem
Method: getFileSystem
Parameters: none
Return value: java.io.FileSystem

To add this method:
- create new file pyjvm/platform/java/io/filesystem.py
- add java_io_FileSystem_getFileSystem___Ljava_io_FileSystem_(frame, args)
- add implementation

For this particular implementation, code will return VMO (VM owned object). And all next
unimplemented calls will go to the implementation of that object.

Rerunning code on and on, these methods will be implemented:

- vmo5_getSeparator___C
- vmo5_getPathSeparator___C
- implement vmo5_normalize__Ljava_lang_String__Ljava_lang_String_
- vmo5_getBooleanAttributes__Ljava_io_File__I

Last one (vmo5_getBooleanAttributes__Ljava_io_File__I) actually implements file system access.
See javadoc for java.io.FileSystem: getBooleanAttributes