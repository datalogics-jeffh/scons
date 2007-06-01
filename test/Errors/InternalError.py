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

__revision__ = "/home/scons/scons/branch.0/baseline/test/Errors/InternalError.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Verify the exit status and error output if an SConstruct file
throws an InternalError.
"""

import TestSCons

test = TestSCons.TestSCons(match = TestSCons.match_re_dotall)

# Test InternalError.
test.write('SConstruct', """
assert not globals().has_key("InternalError")
from SCons.Errors import InternalError
raise InternalError, 'error inside'
""")

test.run(stdout = "scons: Reading SConscript files ...\ninternal error\n",
         stderr = r"""Traceback \((most recent call|innermost) last\):
  File ".+", line \d+, in .+
  File ".+", line \d+, in .+
  File ".+", line \d+, in .+
  File ".+SConstruct", line \d+, in .+
    raise InternalError, 'error inside'
InternalError: error inside
""", status=2)

test.pass_test()
