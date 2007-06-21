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
Verify that we can print .sconsign files with Configure context
info in them (which have different BuildInfo entries).
"""

import os.path

import TestSCons
import TestSConsign

_obj = TestSCons._obj

test = TestSConsign.TestSConsign(match = TestSConsign.match_re)

_sconf_temp_conftest_0_c = os.path.join('.sconf_temp', 'conftest_0.c')

test.write('SConstruct', """
env = Environment()
import os
env.AppendENVPath('PATH', os.environ['PATH'])
conf = Configure(env)
r1 = conf.CheckCHeader( 'math.h' )
env = conf.Finish()
""")

test.run(arguments = '.')

sig_re = r'[0-9a-fA-F]{32}'
date_re = r'\S+ \S+ [ \d]\d \d\d:\d\d:\d\d \d\d\d\d'

# Note:  There's a space at the end of the '.*': line, because the
# Value node being printed actually begins with a newline.  It would
# probably be good to change that to a repr() of the contents.
expect = r"""=== .:
SConstruct: None \d+ \d+
=== .sconf_temp:
conftest_0.c:
        '.*': 
#include "math.h"


        %(sig_re)s \[.*\]
conftest_0%(_obj)s:
        %(_sconf_temp_conftest_0_c)s: %(sig_re)s \d+ \d+
        %(sig_re)s \[.*\]
""" % locals()

test.run_sconsign(arguments = ".sconsign",
                  stdout = expect)

test.pass_test()
