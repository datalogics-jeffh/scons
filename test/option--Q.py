#!/usr/bin/env python
#
# __COPYRIGHT__
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

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

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
MyBuild = Builder(action = r'%(_python_)s build.py $TARGET')
env = Environment(BUILDERS = { 'MyBuild' : MyBuild })
env.MyBuild(target = 'f1.out', source = 'f1.in')
env.MyBuild(target = 'f2.out', source = 'f2.in')
""" % locals())

test.write('f1.in', "f1.in\n")
test.write('f2.in', "f2.in\n")

test.run(arguments = '-Q f1.out f2.out', stdout = """\
%(_python_)s build.py f1.out
%(_python_)s build.py f2.out
""" % locals())
test.fail_test(not os.path.exists(test.workpath('f1.out')))
test.fail_test(not os.path.exists(test.workpath('f2.out')))

# Make sure -q doesn't suppress other messages, too.
test.run(arguments = '-Q -c f1.out f2.out', stdout = """\
Removed f1.out
Removed f2.out
""")
test.fail_test(os.path.exists(test.workpath('f1.out')))
test.fail_test(os.path.exists(test.workpath('f2.out')))

test.pass_test()
