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

__revision__ = "/home/scons/scons/branch.0/baseline/test/TARGETS.py 0.97.D001 2007/05/17 11:35:19 knight"

"""
Test use of the COMMAND_LINE_TARGETS and DEFAULT_TARGETS variables.
"""

import TestSCons

test = TestSCons.TestSCons()



test.write('SConstruct', """
print COMMAND_LINE_TARGETS
print map(str, BUILD_TARGETS)
Default('.')
print COMMAND_LINE_TARGETS
print map(str, BUILD_TARGETS)
""")

test.write('aaa', 'aaa\n')
test.write('bbb', 'bbb\n')

expect = test.wrap_stdout(read_str = "[]\n[]\n[]\n['.']\n",
                          build_str = "scons: `.' is up to date.\n")
test.run(stdout = expect)

expect = test.wrap_stdout(read_str = "['.']\n['.']\n['.']\n['.']\n",
                          build_str = "scons: `.' is up to date.\n")
test.run(arguments = '.', stdout = expect)

expect = test.wrap_stdout(read_str = "['aaa']\n['aaa']\n['aaa']\n['aaa']\n",
                          build_str = "scons: Nothing to be done for `aaa'.\n")
test.run(arguments = 'aaa', stdout = expect)

expect = test.wrap_stdout(read_str = "['bbb', 'aaa']\n['bbb', 'aaa']\n['bbb', 'aaa']\n['bbb', 'aaa']\n",
                          build_str = """\
scons: Nothing to be done for `bbb'.
scons: Nothing to be done for `aaa'.
""")
test.run(arguments = 'bbb ccc=xyz -n aaa', stdout = expect)



test.write('SConstruct', """
env = Environment()
print map(str, DEFAULT_TARGETS)
print map(str, BUILD_TARGETS)
Default('aaa')
print map(str, DEFAULT_TARGETS)
print map(str, BUILD_TARGETS)
env.Default('bbb')
print map(str, DEFAULT_TARGETS)
print map(str, BUILD_TARGETS)
env.Default(None)
print map(str, DEFAULT_TARGETS)
print map(str, BUILD_TARGETS)
env.Default('ccc')
""")

test.write('ccc', "ccc\n")

expect = test.wrap_stdout(build_str = "scons: Nothing to be done for `ccc'.\n",
                          read_str = """\
[]
[]
['aaa']
['aaa']
['aaa', 'bbb']
['aaa', 'bbb']
[]
[]
""")
test.run(stdout = expect)

expect = test.wrap_stdout(build_str = "scons: `.' is up to date.\n",
                          read_str = """\
[]
['.']
['aaa']
['.']
['aaa', 'bbb']
['.']
[]
['.']
""")
test.run(arguments = '.', stdout = expect)



test.write('SConstruct', """\
print map(str, BUILD_TARGETS)
SConscript('SConscript')
print map(str, BUILD_TARGETS)
""")

test.write('SConscript', """\
BUILD_TARGETS.append('sconscript_target')
""")

test.write('command_line_target', "command_line_target\n")
test.write('sconscript_target', "sconscript_target\n")

expect = test.wrap_stdout(read_str = """\
['command_line_target']
['command_line_target', 'sconscript_target']
""",
                          build_str = """\
scons: Nothing to be done for `command_line_target'.
scons: Nothing to be done for `sconscript_target'.
""")
test.run(arguments = 'command_line_target', stdout = expect)



test.pass_test()
