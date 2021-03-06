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
Validate that we can set the PDFTEX string to our own utility, that
the produced .dvi, .aux and .log files get removed by the -c option,
and that we can use this to wrap calls to the real latex utility.
"""

import os
import os.path
import string
import sys
import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('mypdftex.py', r"""
import sys
import os
base_name = os.path.splitext(sys.argv[1])[0]
infile = open(sys.argv[1], 'rb')
pdf_file = open(base_name+'.pdf', 'wb')
aux_file = open(base_name+'.aux', 'wb')
log_file = open(base_name+'.log', 'wb')
for l in infile.readlines():
    if l[0] != '\\':
        pdf_file.write(l)
        aux_file.write(l)
        log_file.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(PDFTEX = r'%(_python_)s mypdftex.py', tools=['pdftex'])
env.PDF(target = 'test.pdf', source = 'test.tex')
""" % locals())

test.write('test.tex', r"""This is a test.
\end
""")

test.run(arguments = 'test.pdf')

test.must_exist('test.pdf')
test.must_exist('test.aux')
test.must_exist('test.log')

test.run(arguments = '-c test.pdf')

test.must_not_exist('test.pdf')
test.must_not_exist('test.aux')
test.must_not_exist('test.log')



pdftex = test.where_is('pdftex')

if pdftex:

    test.write("wrapper.py", """import os
import string
import sys
open('%s', 'wb').write("wrapper.py\\n")
os.system(string.join(sys.argv[1:], " "))
""" % string.replace(test.workpath('wrapper.out'), '\\', '\\\\'))

    test.write('SConstruct', """
import os
ENV = { 'PATH' : os.environ['PATH'] }
foo = Environment(ENV = ENV)
pdftex = foo.Dictionary('PDFTEX')
bar = Environment(ENV = ENV, PDFTEX = r'%(_python_)s wrapper.py ' + pdftex)
foo.PDF(target = 'foo.pdf', source = 'foo.tex')
bar.PDF(target = 'bar', source = 'bar.tex')
""" % locals())

    tex = r"""
This is the %s TeX file.
\end
"""

    test.write('foo.tex', tex % 'foo.tex')

    test.write('bar.tex', tex % 'bar.tex')

    test.run(arguments = 'foo.pdf', stderr = None)

    test.must_not_exist('wrapper.out')

    test.must_exist('foo.pdf')

    test.run(arguments = 'bar.pdf', stderr = None)

    test.must_exist('wrapper.out')

    test.must_exist('bar.pdf')

test.pass_test()
