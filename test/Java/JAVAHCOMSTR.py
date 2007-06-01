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

__revision__ = "/home/scons/scons/branch.0/baseline/test/Java/JAVAHCOMSTR.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Test that the $JAVAHCOMSTR construction variable allows you to configure
the javah output.
"""

import os.path

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

test.subdir('src')



out_file1_h = os.path.join('out', 'file1.h')
out_file2_h = os.path.join('out', 'file2.h')
out_file3_h = os.path.join('out', 'file3.h')



test.write('myjavah.py', r"""
import sys
outfile = open(sys.argv[1], 'wb')
for f in sys.argv[2:]:
    infile = open(f, 'rb')
    for l in filter(lambda l: l != '/*javah*/\n', infile.readlines()):
        outfile.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(TOOLS = ['default', 'javah'],
                  JAVAHCOM = r'%(_python_)s myjavah.py $TARGET $SOURCES',
                  JAVAHCOMSTR = 'Building javah $TARGET from $SOURCES')
env.JavaH(target = 'out', source = 'file1.class')
env.JavaH(target = 'out', source = 'file2.class')
env.JavaH(target = 'out', source = 'file3.class')
""" % locals())

test.write('file1.class', "file1.class\n/*javah*/\n")
test.write('file2.class', "file2.class\n/*javah*/\n")
test.write('file3.class', "file3.class\n/*javah*/\n")

test.run(stdout = test.wrap_stdout("""\
Building javah %(out_file1_h)s from file1.class
Building javah %(out_file2_h)s from file2.class
Building javah %(out_file3_h)s from file3.class
""" % locals()))

test.must_match(['out', 'file1.h'], "file1.class\n")
test.must_match(['out', 'file2.h'], "file2.class\n")
test.must_match(['out', 'file3.h'], "file3.class\n")



test.pass_test()
