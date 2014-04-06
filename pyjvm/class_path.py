# PyJVM (pyjvm.org) Java Virtual Machine implemented in pure Python
# Copyright (C) 2014 Andrew Romanenco (andrew@romanenco.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''Class path for jar files and directories. Cache all jars content.
JAVA_HOME must be set.

Class path is list of jar files and folders for classes lookup.
Separator ":", (";", ",") are also supported

See START.txt for details
'''

import os
import zipfile


def read_class_path(class_path):
    '''Cache content of all jars.
    Begin with rt.jar
    '''

    # folders for lookup for class files
    lookup_paths = []
    # content of all jars (name->path to jar)
    jars = {}
    # content of rt.jar
    rt = {}

    # first check local rt.jar
    local_path = os.path.dirname(os.path.realpath(__file__))
    RT_JAR = os.path.join(local_path, "../rt/rt.jar")
    if not os.path.isfile(RT_JAR):
        JAVA_HOME = os.environ.get('JAVA_HOME')
        if JAVA_HOME is None:
            raise Exception("JAVA_HOME is not set")
        if not os.path.isdir(JAVA_HOME):
            raise Exception("JAVA_HOME must be a folder: %s" % JAVA_HOME)

        RT_JAR = os.path.join(JAVA_HOME, "lib/rt.jar")
        if not os.path.exists(RT_JAR) or os.path.isdir(RT_JAR):
            RT_JAR = os.path.join(JAVA_HOME, "jre/lib/rt.jar")
            if not os.path.exists(RT_JAR) or os.path.isdir(RT_JAR):
                raise Exception("rt.jar not found")

    if not zipfile.is_zipfile(RT_JAR):
        raise Exception("rt.jar is not a zip: %s" % RT_JAR)

    read_from_jar(RT_JAR, rt)

    current = os.getcwd()

    splitter = None
    if ":" in class_path:
        splitter = ":"
    elif ";" in class_path:
        splitter = ";"
    elif "," in class_path:
        splitter = ","
    else:
        splitter = ":"
    cpaths = class_path.split(splitter)
    for p in cpaths:
        p = p.strip()
        path = os.path.join(current, p)
        if not os.path.exists(path):
            raise Exception("Wrong class path entry: %s (path not found %s)",
                            p, path)
        if os.path.isdir(path):
            lookup_paths.append(path)
        else:
            if zipfile.is_zipfile(path):
                read_from_jar(path, jars)
            else:
                raise Exception("Class path entry %s is not a jar file" % path)

    return (lookup_paths, jars, rt)


def read_from_jar(jar, dict_data):
    '''Read file list from a jar'''
    if not zipfile.is_zipfile(jar):
        raise Exception("Not a jar file: %s" % jar)
    with zipfile.ZipFile(jar, "r") as j:
        for name in j.namelist():
            if name.endswith(".class"):  # at some point save all files
                dict_data[name] = jar
