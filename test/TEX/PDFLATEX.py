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

__revision__ = "/home/scons/scons/branch.0/baseline/test/TEX/PDFLATEX.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Validate that we can set the PDFLATEX string to our own utility, that
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



test.write('mypdflatex.py', r"""
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
env = Environment(PDFLATEX = r'%(_python_)s mypdflatex.py', tools=['pdflatex'])
env.PDF(target = 'test1.pdf', source = 'test1.ltx')
env.PDF(target = 'test2.pdf', source = 'test2.latex')
""" % locals())

test.write('test1.ltx', r"""This is a .ltx test.
\end
""")

test.write('test2.latex', r"""This is a .latex test.
\end
""")

test.run(arguments = '.')

test.must_exist('test1.pdf')
test.must_exist('test1.aux')
test.must_exist('test1.log')

test.must_exist('test2.pdf')
test.must_exist('test2.aux')
test.must_exist('test2.log')

test.run(arguments = '-c .')

test.must_not_exist('test1.pdf')
test.must_not_exist('test1.aux')
test.must_not_exist('test1.log')

test.must_not_exist('test2.pdf')
test.must_not_exist('test2.aux')
test.must_not_exist('test2.log')



pdflatex = test.where_is('pdflatex')

if pdflatex:

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
pdflatex = foo.Dictionary('PDFLATEX')
bar = Environment(ENV = ENV, PDFLATEX = r'%(_python_)s wrapper.py ' + pdflatex)
foo.PDF(target = 'foo.pdf', source = 'foo.ltx')
bar.PDF(target = 'bar', source = 'bar.latex')
""" % locals())

    latex = r"""
\documentclass{letter}
\begin{document}
This is the %s LaTeX file.
\end{document}
"""

    test.write('foo.ltx', latex % 'foo.ltx')

    test.write('bar.latex', latex % 'bar.latex')

    test.run(arguments = 'foo.pdf', stderr = None)

    test.must_not_exist('wrapper.out')

    test.must_exist('foo.pdf')

    test.run(arguments = 'bar.pdf', stderr = None)

    test.must_match('wrapper.out', "wrapper.py\n")

    test.must_exist('bar.pdf')

test.pass_test()
