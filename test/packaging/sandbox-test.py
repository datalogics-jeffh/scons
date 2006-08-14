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
Test a simple project
"""

import os
import TestSCons

python = TestSCons.python

test = TestSCons.TestSCons()

tar = test.detect('TAR', 'tar')

if tar:
   test.subdir('src')

   test.write([ 'src', 'foobar.h' ], '')
   test.write([ 'src', 'foobar.c' ], '')

   test.write('SConstruct', """
from glob import glob

src_files = glob( 'src/*.c' )
include_files = glob( 'src/*.h' )

SharedLibrary( 'foobar', src_files )

Package( projectname = 'libfoobar',
         version     = '1.2.3',
         type        = 'targz',
         source      = src_files + include_files )

Package( projectname = 'libfoobar',
         version     = '1.2.3',
         type        = 'zip',
         source      = src_files + include_files )
""")

   test.run(stderr=None)

   test.fail_test( not os.path.exists( 'libfoobar-1.2.3.tar.gz' ) )
   test.fail_test( not os.path.exists( 'libfoobar-1.2.3.zip' ) )

test.pass_test()
