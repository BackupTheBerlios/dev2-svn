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

import time
import unittest

from dev2lib.action import ACTIONS
from dev2lib.net.session import Session, STATUS


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.addr = ("localhost", 59334)
        self.s1 = Session(connection_handler=self.dummy_conn_handler)
        self.s1.listen(self.addr)
        self.s1.set_global_handler(self.global_handler_s1)
        self.s2 = Session()
        self.s2.set_global_handler(self.global_handler_s2)

    def dummy_conn_handler(self, session):
        print "new connexion"

    def global_handler_s1(self, action):
        if action.action == ACTIONS['start']:
            self.s1.accept_start()
        else:
            print "Got unknown action %s" % str(action)

    def global_handler_s2(self, action):
        if action.action == ACTIONS['accept_start']:
            if self.s2.status == STATUS['connecting']:
                self.s2.status = STATUS['connected']
        else:
            print "Got unknown action %s" % str(action)

    def testStartSession(self):
        count = 10
        self.failUnless(self.s2.start(self.addr))
        time.sleep(0.3) # wait a little for the socket to be created
        while self.s2.status == STATUS['connecting'] and count > 0:
            self.s1.check()
            count -= 1
            time.sleep(0.01)
        self.s2.check()
        self.failUnlessEqual(self.s1.status, STATUS['connected'])
        self.failUnlessEqual(self.s1.status, self.s2.status)

    def tearDown(self):
        self.s2.close()
        self.s1.close()

def main():
    unittest.main()

if __name__ == "__main__":
    main()
