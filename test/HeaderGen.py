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

__revision__ = "/home/scons/scons/branch.0/baseline/test/HeaderGen.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Test that dependencies in generated header files get re-scanned correctly
and that generated header files don't cause circular dependencies.
"""

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """\
def writeFile(target, contents):
    file = open(str(target[0]), 'wb')
    file.write(contents)
    file.close()
    return 0

env = Environment()
libgen = env.StaticLibrary('gen', 'gen.cpp')
Default(libgen)
env.Command('gen2.h', [],
            lambda env,target,source: writeFile(target, 'int foo = 3;\\n'))
env.Command('gen.h', [],
            lambda env,target,source: writeFile(target, '#include "gen2.h"\\n'))
env.Command('gen.cpp', [],
            lambda env,target,source: writeFile(target, '#include "gen.h"\\n'))
""")

test.run(stderr=TestSCons.noisy_ar,
         match=TestSCons.match_re_dotall)

test.up_to_date(arguments = '.')

test.write('SConstruct', """\
env = Environment()

def gen_a_h(target, source, env):
    t = open(str(target[0]), 'wb')
    s = open(str(source[0]), 'rb')
    s.readline()
    t.write(s.readline()[:-1] + ';\\n')

MakeHeader = Builder(action = gen_a_h)
env_no_scan = env.Clone(SCANNERS=[], BUILDERS={'MakeHeader' : MakeHeader})
env_no_scan.MakeHeader('a.h', 'a.c')

env.StaticObject('a.c')
""")

test.write('a.c', """\
#include "a.h"
void a(void)
{
        ;
}
""")

test.run()

test.pass_test()
