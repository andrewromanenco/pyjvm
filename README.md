Work in progress.

Refactoring code to improve structure and support python 3.

Testing

Run all tests: python3 -m unittest discover
Run module test: python3 -m unittest tests.test_class_parser
Run single test: python3 -m unittest tests.test_class_parser.TestClassParser.test_parse_does_not_fail_with_good_input
Run pylint: python3 -m pylint path_to_file

From now on, sources are reformatted with yapf
https://github.com/google/yapf

Before commit:

 - yapf -i path to file
 - run tests again
 - commit
