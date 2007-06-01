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

__revision__ = "/home/scons/scons/branch.0/baseline/test/YACC/YACCHXXFILESUFFIX.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Test that setting the YACCHXXFILESUFFIX variable can reflect a yacc
utility that writes to an odd
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('myyacc.py', """\
import getopt
import os.path
import string
import sys
opts, args = getopt.getopt(sys.argv[1:], 'do:')
for o, a in opts:
    if o == '-o':
        outfile = open(a, 'wb')
for f in args:
    infile = open(f, 'rb')
    for l in filter(lambda l: l != '/*yacc*/\\n', infile.readlines()):
        outfile.write(l)
outfile.close()
base, ext = os.path.splitext(args[0])
open(base+'.hxxsuffix', 'wb').write(string.join(sys.argv)+'\\n')
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(tools=['default', 'yacc'],
                  YACC = r'%(_python_)s myyacc.py',
                  YACCFLAGS = '-d',
                  YACCHXXFILESUFFIX = '.hxxsuffix')
env.CXXFile(target = 'aaa', source = 'aaa.yy')
""" % locals())

test.write('aaa.yy', "aaa.yy\n/*yacc*/\n")

test.run(arguments = '.')

test.must_match('aaa.cc', "aaa.yy\n")
test.must_match('aaa.hxxsuffix', "myyacc.py -d -o aaa.cc aaa.yy\n")

test.up_to_date(arguments = '.')



test.pass_test()
