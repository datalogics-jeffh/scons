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

"""
Test the BoolOption canned Option type.
"""

import os.path
import string

try:
    True, False
except NameError:
    True = (0 == 0)
    False = (0 != 0)

import TestSCons

test = TestSCons.TestSCons()

SConstruct_path = test.workpath('SConstruct')

def check(expect):
    result = string.split(test.stdout(), '\n')
    assert result[1:len(expect)+1] == expect, (result[1:len(expect)+1], expect)



test.write(SConstruct_path, """\
from SCons.Options import BoolOption

opts = Options(args=ARGUMENTS)
opts.AddOptions(
    BoolOption('warnings', 'compilation with -Wall and similiar', 1),
    BoolOption('profile', 'create profiling informations', 0),
    )

env = Environment(options=opts)
Help(opts.GenerateHelpText(env))

print env['warnings']
print env['profile']

Default(env.Alias('dummy', None))
""")



test.run()
check([str(True), str(False)])

test.run(arguments='warnings=0 profile=no profile=true')
check([str(False), str(True)])

expect_stderr = """
scons: *** Error converting option: warnings
Invalid value for boolean option: irgendwas
File "%(SConstruct_path)s", line 9, in ?
""" % locals()

test.run(arguments='warnings=irgendwas', stderr = expect_stderr, status=2)



test.pass_test()
