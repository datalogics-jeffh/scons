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

__revision__ = "/home/scons/scons/branch.0/baseline/test/DVIPDF/makeindex.py 0.97.D001 2007/05/17 11:35:19 knight"

import TestSCons

test = TestSCons.TestSCons()



dvipdf = test.where_is('dvipdf')
tex = test.where_is('tex')

if not dvipdf or not tex:
    test.skip_test('Could not find dvipdf or text; skipping test(s).\n')



test.write('SConstruct', """
import os
env = Environment(ENV = { 'PATH' : os.environ['PATH'] })
dvipdf = env.Dictionary('DVIPDF')
env.PDF(target = 'foo.pdf',
        source = env.DVI(target = 'foo.dvi', source = 'foo.tex'))
""")

test.write('foo.tex', r"""
\documentclass{article}
\usepackage{makeidx}
\makeindex

\begin{document}
\section{Test 1}
I would like to \index{index} this.

\section{test 2}
I'll index \index{this} as well.

\printindex
\end{document}
""")

test.run(arguments = 'foo.pdf', stderr = None)

test.must_exist(test.workpath('foo.pdf'))



test.pass_test()
