#!/usr/bin/env python
#
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "/home/scons/scons/branch.0/baseline/test/scons-time/obj/chdir.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Verify that the obj -C and --chdir options change directory before
globbing for files.
"""

import os.path

import TestSCons_time

test = TestSCons_time.TestSCons_time()

test.subdir('logs')

lines = [
    '    pre-read    post-read    pre-build   post-build\n'
]

line_fmt = '       1101%(i)s        1102%(i)s        1103%(i)s        1104%(i)s    %(logfile_name)s\n'

for i in xrange(9):
    logfile_name = os.path.join('logs', 'foo-%s.log' % i)
    test.fake_logfile(logfile_name, i)
    lines.append(line_fmt % locals())

expect = ''.join(lines)

test.run(arguments = 'obj -C logs Environment.Base foo-*.log', stdout = expect)

test.run(arguments = 'obj --chdir logs Environment.Base foo-?.log', stdout = expect)

test.pass_test()
