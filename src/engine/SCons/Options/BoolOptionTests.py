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

__revision__ = "/home/scons/scons/branch.0/baseline/src/engine/SCons/Options/BoolOptionTests.py 0.97.D001 2007/05/17 11:35:19 knight"

import SCons.compat

import sys
import unittest

import SCons.Errors
import SCons.Options

class BoolOptionTestCase(unittest.TestCase):
    def test_BoolOption(self):
        """Test BoolOption creation"""
        opts = SCons.Options.Options()
        opts.Add(SCons.Options.BoolOption('test', 'test option help', 0))

        o = opts.options[0]
        assert o.key == 'test', o.key
        assert o.help == 'test option help (yes|no)', o.help
        assert o.default == 0, o.default
        assert not o.validator is None, o.validator
        assert not o.converter is None, o.converter

    def test_converter(self):
        """Test the BoolOption converter"""
        opts = SCons.Options.Options()
        opts.Add(SCons.Options.BoolOption('test', 'test option help', 0))

        o = opts.options[0]

        true_values = [
                'y',    'Y',
                'yes',  'YES',
                't',    'T',
                'true', 'TRUE',
                'on',   'ON',
                'all',  'ALL',
                '1',
        ]
        false_values = [
                'n',    'N',
                'no',   'NO',
                'f',    'F',
                'false', 'FALSE',
                'off',  'OFF',
                'none', 'NONE',
                '0',
        ]

        for t in true_values:
            x = o.converter(t)
            assert x, "converter returned false for '%s'" % t

        for f in false_values:
            x = o.converter(f)
            assert not x, "converter returned true for '%s'" % f

        caught = None
        try:
            o.converter('x')
        except ValueError:
            caught = 1
        assert caught, "did not catch expected ValueError"

    def test_validator(self):
        """Test the BoolOption validator"""
        opts = SCons.Options.Options()
        opts.Add(SCons.Options.BoolOption('test', 'test option help', 0))

        o = opts.options[0]

        env = {
            'T' : True,
            'F' : False,
            'N' : 'xyzzy',
        }

        o.validator('T', 0, env)

        o.validator('F', 0, env)

        caught = None
        try:
            o.validator('N', 0, env)
        except SCons.Errors.UserError:
            caught = 1
        assert caught, "did not catch expected UserError for N"

        caught = None
        try:
            o.validator('NOSUCHKEY', 0, env)
        except KeyError:
            caught = 1
        assert caught, "did not catch expected KeyError for NOSUCHKEY"


if __name__ == "__main__":
    suite = unittest.makeSuite(BoolOptionTestCase, 'test_')
    if not unittest.TextTestRunner().run(suite).wasSuccessful():
        sys.exit(1)
