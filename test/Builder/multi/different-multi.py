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

__revision__ = "/home/scons/scons/branch.0/baseline/test/Builder/multi/different-multi.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Verify that trying to call a target with two different "multi" builders
generates an error.
"""

import TestSCons

test = TestSCons.TestSCons(match=TestSCons.match_re)

test.write('SConstruct', """\
def build(env, target, source):
    file = open(str(target[0]), 'wb')
    for s in source:
        file.write(open(str(s), 'rb').read())

def build2(env, target, source):
    build(env, target, source)

# Put the names on the Builder objects and in the environment so
# the error output should be consistent regardless of Python version
# or how we mess with the Builder internals.
B = Builder(action=build, multi=1, name='B')
C = Builder(action=build2, multi=1, name='C')
env = Environment(BUILDERS = { 'B' : B, 'C' : C })
env.B(target = 'file8.out', source = 'file8.in')
env.C(target = 'file8.out', source = 'file8.in')
""")

test.write('file8a.in', 'file8a.in\n')
test.write('file8b.in', 'file8b.in\n')

expect = TestSCons.re_escape("""
scons: *** Two different builders (B and C) were specified for the same target: file8.out
""") + TestSCons.file_expr

test.run(arguments='file8.out', status=2, stderr=expect)

test.pass_test()
