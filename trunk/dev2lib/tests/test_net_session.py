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

from dev2lib.net.session import Session

class ServerTests(unittest.TestCase):
    def setUp(self):
        addr = ("localhost", 59334)
        self.s1 = Session()
        self.s1.listen(addr)
        self.s2 = Session()
        self.s2.connect(addr)

    def tearDown(self):
        self.s2.close()
        self.s1.close()

def main():
    unittest.main()

if __name__ == "__main__":
    main()
