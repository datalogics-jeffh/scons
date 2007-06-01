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

__revision__ = "/home/scons/scons/branch.0/baseline/test/PRINT_CMD_LINE_FUNC.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Test the PRINT_CMD_LINE_FUNC construction variable.
"""

import string
import sys
import TestCmd
import TestSCons

_exe = TestSCons._exe
_obj = TestSCons._obj

test = TestSCons.TestSCons(match = TestCmd.match_re)


test.write('SConstruct', r"""
import sys
def print_cmd_line(s, target, source, env):
    sys.stdout.write("BUILDING %s from %s with %s\n"%
                     (str(target[0]), str(source[0]), s))

e = Environment(PRINT_CMD_LINE_FUNC=print_cmd_line)
e.Program(target = 'prog', source = 'prog.c')
""")

test.write('prog.c', r"""
int main(int argc, char *argv[]) { return 0; }
""")

test.run(arguments = '-Q .')

expected_lines = [
    "BUILDING prog%s from prog.c with" % (_obj,),
    "BUILDING prog%s from prog%s with" % (_exe, _obj),
]

missing_lines = filter(lambda l: string.find(test.stdout(), l) == -1,
                       expected_lines)
if missing_lines:
    print "Expected the following lines in STDOUT:"
    print "\t" + string.join(expected_lines, "\n\t")
    print "ACTUAL STDOUT =========="
    print test.stdout()
    test.fail_test(1)

test.run(arguments = '-c .')

# Just make sure it doesn't blow up when PRINT_CMD_LINE_FUNC
# is explicity initialized to None.
test.write('SConstruct', r"""
e = Environment(PRINT_CMD_LINE_FUNC=None)
e.Program(target = 'prog', source = 'prog.c')
""")

test.run(arguments = '-Q .')

test.pass_test()
