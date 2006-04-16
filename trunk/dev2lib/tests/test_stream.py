# Dev2 - pair programming development tool
# Copyright (C) 2005-2006 Alexandre Saint <stalst@gmail.com>

# This file is part of Dev2.

# Dev2 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# Dev2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Test cases for the creation of streams."""

import unittest

from dev2lib.action import StartAction, AcceptStartAction
from dev2lib.stream import XMLStream, TextStream

class XMLStreamProtocolv1Tests(unittest.TestCase):
    def testStartAction(self):
        expected = u'<stream version="1"><action>1</action><name/></stream>'
        action = StartAction()
        stream = XMLStream.make_stream(action)
        self.assertEqual(expected, stream)

    def testAcceptAction(self):
        expected = u'<stream version="1"><action>2</action>' \
                '<name>john</name></stream>'
        action = AcceptStartAction(name="john")
        stream = XMLStream.make_stream(action)
        self.assertEqual(expected, stream)

class TextStreamProtocolv1Tests(unittest.TestCase):
    def testStartAction(self):
        expected = u'P2P 1 1 '
        action = StartAction()
        stream = TextStream.make_stream(action)
        self.assertEqual(expected.lower(), stream.lower())

    def testAcceptAction(self):
        expected = u'P2P 1 2 john'
        action = AcceptStartAction(name="john")
        stream = TextStream.make_stream(action)
        self.assertEqual(expected.lower(), stream.lower())

def suites():
    suites = [
        unittest.makeSuite(XMLStreamProtocolv1Tests),
        unittest.makeSuite(TextStreamProtocolv1Tests),
        ]
    return suites

def main():
    unittest.main()

if __name__ == "__main__":
    main()
