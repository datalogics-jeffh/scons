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

__revision__ = "/home/scons/scons/branch.0/baseline/test/runtest/testlistfile.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Test a list of tests to run in a file specified with the -f option.
"""

import os.path

import TestCmd
import TestRuntest

test_fail_py = os.path.join('test', 'fail.py')
test_no_result_py = os.path.join('test', 'no_result.py')
test_pass_py = os.path.join('test', 'pass.py')

test = TestRuntest.TestRuntest()

test.subdir('test')

test.write_failing_test(['test', 'fail.py'])

test.write_no_result_test(['test', 'no_result.py'])

test.write_passing_test(['test', 'pass.py'])

test.write('t.txt', """\
#%(test_fail_py)s
%(test_pass_py)s
""" % locals())

# NOTE:  The "test/fail.py : FAIL" and "test/pass.py : PASS" lines both
# have spaces at the end.

expect = """qmtest.py run --output results.qmr --format none --result-stream="scons_tdb.AegisChangeStream" %(test_pass_py)s
--- TEST RESULTS -------------------------------------------------------------

  %(test_pass_py)s                                  : PASS    

--- TESTS THAT DID NOT PASS --------------------------------------------------

  None.


--- STATISTICS ---------------------------------------------------------------

       1        tests total

       1 (100%%) tests PASS
""" % locals()

test.run(arguments = '-f t.txt', stdout = expect)

test.pass_test()
