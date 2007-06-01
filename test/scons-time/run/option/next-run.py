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

__revision__ = "/home/scons/scons/branch.0/baseline/test/scons-time/run/option/next-run.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Verify that the script finds the next run number based on the
contents of the directory, even when specified with --outdir.
"""

import TestSCons_time

test = TestSCons_time.TestSCons_time()

test.subdir('sub')

test.write_fake_scons_py()

test.write_sample_project('foo.tar.gz')

test.run(arguments = 'run foo.tar.gz')

test.must_exist('foo-000-0.log',
                'foo-000-0.prof',
                'foo-000-1.log',
                'foo-000-1.prof',
                'foo-000-2.log',
                'foo-000-2.prof')

test.must_not_exist('foo-001-0.log',
                    'foo-001-0.prof',
                    'foo-001-1.log',
                    'foo-001-1.prof',
                    'foo-001-2.log',
                    'foo-001-2.prof')

test.run(arguments = 'run foo.tar.gz')

test.must_exist('foo-001-0.log',
                'foo-001-0.prof',
                'foo-001-1.log',
                'foo-001-1.prof',
                'foo-001-2.log',
                'foo-001-2.prof')

test.must_not_exist('foo-002-0.log',
                    'foo-002-0.prof',
                    'foo-002-1.log',
                    'foo-002-1.prof',
                    'foo-002-2.log',
                    'foo-002-2.prof')

test.run(arguments = 'run foo.tar.gz')

test.must_exist('foo-002-0.log',
                'foo-002-0.prof',
                'foo-002-1.log',
                'foo-002-1.prof',
                'foo-002-2.log',
                'foo-002-2.prof')

test.run(arguments = 'run --outdir sub foo.tar.gz')

test.must_exist(['sub', 'foo-000-0.log'],
                ['sub', 'foo-000-0.prof'],
                ['sub', 'foo-000-1.log'],
                ['sub', 'foo-000-1.prof'],
                ['sub', 'foo-000-2.log'],
                ['sub', 'foo-000-2.prof'])

test.must_not_exist('foo-003-0.log',
                    'foo-003-0.prof',
                    'foo-003-1.log',
                    'foo-003-1.prof',
                    'foo-003-2.log',
                    'foo-003-2.prof')

test.pass_test()
