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

__revision__ = "/home/scons/scons/branch.0/baseline/test/option--.py 0.97.D001 2007/05/17 11:35:19 knight"

import os.path
import string
import sys
import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

test.write('build.py', r"""
import sys
file = open(sys.argv[1], 'wb')
file.write("build.py: %s\n" % sys.argv[1])
file.close()
""")

test.write('SConstruct', """
MyBuild = Builder(action = r'%(_python_)s build.py $TARGETS')
env = Environment(BUILDERS = { 'MyBuild' : MyBuild })
env.MyBuild(target = '-f1.out', source = 'f1.in')
env.MyBuild(target = '-f2.out', source = 'f2.in')
""" % locals())

test.write('f1.in', "f1.in\n")
test.write('f2.in', "f2.in\n")

expect = test.wrap_stdout('%(_python_)s build.py -f1.out\n%(_python_)s build.py -f2.out\n' % locals())

test.run(arguments = '-- -f1.out -f2.out', stdout = expect)

test.fail_test(not os.path.exists(test.workpath('-f1.out')))
test.fail_test(not os.path.exists(test.workpath('-f2.out')))

test.pass_test()

