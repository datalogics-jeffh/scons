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

__revision__ = "/home/scons/scons/branch.0/baseline/test/Builder/multi/different-actions.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Verify that environments with actions that have different signatures
generate an error.
"""

import TestSCons

test = TestSCons.TestSCons(match=TestSCons.match_re)

test.write('SConstruct', """\
def build(env, target, source):
    file = open(str(target[0]), 'wb')
    for s in source:
        file.write(open(str(s), 'rb').read())

B = Builder(action=Action(build, varlist=['XXX']), multi=1)
env = Environment(BUILDERS = { 'B' : B }, XXX = 'foo')
env2 = env.Clone(XXX = 'var')
env.B(target = 'file6.out', source = 'file6a.in')
env2.B(target = 'file6.out', source = 'file6b.in')
""")

test.write('file6a.in', 'file6a.in\n')
test.write('file6b.in', 'file6b.in\n')

expect = TestSCons.re_escape("""
scons: *** Two environments with different actions were specified for the same target: file6.out
""") + TestSCons.file_expr

test.pass_test()

test.run(arguments='file6.out', status=2, stderr=expect)

test.pass_test()
