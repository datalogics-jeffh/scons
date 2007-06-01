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

__revision__ = "/home/scons/scons/branch.0/baseline/src/engine/SCons/PathListTests.py 0.97.D001 2007/05/17 11:35:19 knight"

import sys
import unittest

import SCons.PathList


class subst_pathTestCase(unittest.TestCase):

    def setUp(self):

        class FakeEnvironment:
            def __init__(self, **kw):
                self.kw = kw
            def subst(self, s, target=None, source=None, conv=lambda x: x):
                if s[0] == '$':
                    s = s[1:]
                    if s == 'target':
                        s = target
                    elif s == 'source':
                        s = source
                    else:
                        s = self.kw[s]
                return s

        self.env = FakeEnvironment(AAA = 'aaa')

    def test_node(self):
        """Test the subst_path() method on a Node
        """

        import SCons.Node

        class A:
            pass

        n = SCons.Node.Node()

        pl = SCons.PathList.PathList((n,))

        result = pl.subst_path(self.env, 'y', 'z')

        assert result == (n,), result

    def test_object(self):
        """Test the subst_path() method on a non-Node object
        """

        class A:
            def __str__(self):
                return '<object A>'

        a = A()

        pl = SCons.PathList.PathList((a,))

        result = pl.subst_path(self.env, 'y', 'z')

        assert result == ('<object A>',), result

    def test_object_get(self):
        """Test the subst_path() method on an object with a get() method
        """

        class B:
            def get(self):
                return 'b'

        b = B()

        pl = SCons.PathList.PathList((b,))

        result = pl.subst_path(self.env, 'y', 'z')

        assert result == ('b',), result

    def test_string(self):
        """Test the subst_path() method on a non-substitution string
        """

        self.env.subst = lambda s, target, source, conv: 'NOT THIS STRING'

        pl = SCons.PathList.PathList(('x'))

        result = pl.subst_path(self.env, 'y', 'z')

        assert result == ('x',), result

    def test_subst(self):
        """Test the subst_path() method on a substitution string
        """

        pl = SCons.PathList.PathList(('$AAA',))

        result = pl.subst_path(self.env, 'y', 'z')

        assert result == ('aaa',), result


class PathListCacheTestCase(unittest.TestCase):

    def test_no_PathListCache(self):
        """Make sure the PathListCache class is not visible
        """
        try:
            SCons.PathList.PathListCache
        except AttributeError:
            pass
        else:
            self.fail("Found PathListCache unexpectedly\n")


class PathListTestCase(unittest.TestCase):

    def test_PathList(self):
        """Test the PathList() entry point
        """

        x1 = SCons.PathList.PathList(('x',))
        x2 = SCons.PathList.PathList(['x',])

        assert x1 is x2, (x1, x2)

        x3 = SCons.PathList.PathList('x')

        assert not x1 is x3, (x1, x3)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    tclasses = [
        subst_pathTestCase,
        PathListCacheTestCase,
        PathListTestCase,
    ]
    for tclass in tclasses:
        names = unittest.getTestCaseNames(tclass, 'test_')
        suite.addTests(map(tclass, names))
    if not unittest.TextTestRunner().run(suite).wasSuccessful():
        sys.exit(1)
