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

__revision__ = "/home/scons/scons/branch.0/baseline/test/CC/CCFLAGS.py 0.97.D001 2007/05/17 11:35:19 knight"

import sys
import TestSCons

if sys.platform == 'win32':
    _obj = '.obj'
    fooflags = '/nologo -DFOO'
    barflags = '/nologo -DBAR'
else:
    _obj = '.o'
    fooflags = '-DFOO'
    barflags = '-DBAR'

test = TestSCons.TestSCons()

test.write('SConstruct', """
foo = Environment(CCFLAGS = '%s')
bar = Environment(CCFLAGS = '%s')
foo.Object(target = 'foo%s', source = 'prog.c')
bar.Object(target = 'bar%s', source = 'prog.c')
foo.Program(target = 'foo', source = 'foo%s')
bar.Program(target = 'bar', source = 'bar%s')
foo.Program(target = 'prog', source = 'prog.c',
            CCFLAGS = '$CCFLAGS -DBAR $BAZ', BAZ = '-DBAZ')
""" % (fooflags, barflags, _obj, _obj, _obj, _obj))

test.write('prog.c', r"""
#include <stdio.h>
#include <stdlib.h>

int
main(int argc, char *argv[])
{
        argv[argc++] = "--";
#ifdef FOO
        printf("prog.c:  FOO\n");
#endif
#ifdef BAR
        printf("prog.c:  BAR\n");
#endif
#ifdef BAZ
        printf("prog.c:  BAZ\n");
#endif
        exit (0);
}
""")


test.run(arguments = '.')

test.run(program = test.workpath('foo'), stdout = "prog.c:  FOO\n")
test.run(program = test.workpath('bar'), stdout = "prog.c:  BAR\n")
test.run(program = test.workpath('prog'), stdout = """\
prog.c:  FOO
prog.c:  BAR
prog.c:  BAZ
""")

test.write('SConstruct', """
bar = Environment(CCFLAGS = '%s')
bar.Object(target = 'foo%s', source = 'prog.c')
bar.Object(target = 'bar%s', source = 'prog.c')
bar.Program(target = 'foo', source = 'foo%s')
bar.Program(target = 'bar', source = 'bar%s')
""" % (barflags, _obj, _obj, _obj, _obj))

test.run(arguments = '.')

test.run(program = test.workpath('foo'), stdout = "prog.c:  BAR\n")
test.run(program = test.workpath('bar'), stdout = "prog.c:  BAR\n")

test.pass_test()
