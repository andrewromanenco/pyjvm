At this point all java byte code operations are already implemented.
But many native handlers are not. See natives.md for details.

To find which methods to implement, run you sample java program and check
if it will finish with an exception:

> Exception: Op (SOME_NAME) is not yet supported in natives

This exception is good starting point to start coding from.

Docs:
natives.md - overall overview
sample_dev.md - use case for adding new native methods

Make sure you are using pep8 and pylint for code verification.

I would really advise to contact me first, to discuss details of
your implementation.

Andrew Romanenco
andrew@romanenco.com
