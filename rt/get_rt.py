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
'''rt.jar downloader.
For systems without java installed.
'''

import urllib2

# Dropbox content, this is rt.jar from JDK7
url = 'https://dl.dropboxusercontent.com/s/9wiumk3xvigqndi/rt.jar'

print "rt.jar from Java 7 is being downloaded"

u = urllib2.urlopen(url)
f = open('rt.jar', 'wb')
meta_info = u.info()
file_size = int(meta_info.getheaders("Content-Length")[0])
print "Total: %s mb" % (file_size/1024/1024)

downloaded = 0
block = 8192
print " [" + ("="*50) + "]"
while True:
    data = u.read(block)
    if not data:
        break

    downloaded += len(data)
    f.write(data)
    completed = downloaded * 100.0 / file_size
    arrow = "=" * int(completed/2.0)
    status = r"[%s] %3.0f%%" % (arrow, completed)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()
