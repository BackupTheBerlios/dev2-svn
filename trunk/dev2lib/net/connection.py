# -*- coding: iso-8859-1 -*-

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

"""
"""

import logging
import select
import socket

from dev2lib.action import ActionFactory
from dev2lib.stream import TextStream


log = logging.getLogger("dev2lib.net.connection")
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s:" +
        " %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)



class Connection(object):
    def __init__(self, socket=None):
        """
        Arguments:
            socket -- (optionel) un object socket valide
        """
        log.info("Initializing connection")

        self.socket = socket
        if self.socket is not None:
            # XXX An improvement would be to check the validity of the socket.
            self.socket.setblocking(0)
            log.debug("peername %s" % str(socket.getpeername()))


    def connect(self, addr):
        """Connexion à un hôte distant.

        Arguments:
            addr -- tuple (host, port)
        """
        # Fermer une éventuelle connexion établie auparavant.
        self.disconnect()

        # Créer un nouveau socket TCP.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            log.info("Connecting to %s on port %d ..." % addr)
            # Essayer de se connecter.
            self.socket.connect(addr)
            self.socket.setblocking(0)
        except socket.error:
            log.exception("Connection failed")
            self.socket = None

        return self.is_connected()

    def disconnect(self):
        """Fermer la connexion."""
        if self.is_connected():
            try:
                log.info("Disconnecting...")
                self.socket.close()
                self.socket = None
            except socket.error:
                log.warning("Error while disconnecting")
                self.socket = None
            except:
                log.warning("Error while disconnecting")
                self.socket = None

    def is_connected(self):
        """Retourne True ou False en fonction de l'état de la connexion."""
        return (self.socket is not None)

    def get_socket(self):
        return self.socket


class PairProgConnection(Connection):
    """Implémente les commandes de communication "pair-programming" avec le
    client.
    """
    _select_timeout = 0.1

    def __init__(self, socket=None):
        Connection.__init__(self, socket=socket)
        self.buffer = ""
        self._actions = []

    def send_stream(self, action):
        """Send a text stream representing the action."""
        data = TextStream.make_stream(action)
        log.debug(u"TO PEER: %s" % data)
        size = 0
        while size < len(data):
            data = data[size:]
            size = self.socket.send(data)
        return size

    def get_actions(self):
        actions = self._actions
        self._actions = []
        return actions

    def iter_actions(self):
        """Iterate over the stored actions returning them one by one."""
        for i in range(len(self._actions)):
            yield self._actions[i]
            # delete this action when we're sure it has been received
            del self._actions[i]
        raise StopIteration

    def has_streams(self):
        """Check if new streams have been received on the socket."""
        n_streams = self._extract_streams()
        return n_streams != 0

    def _extract_streams(self):
        """Extract new streams from the buffer if any."""
        if not self._pull_data():
            return 0

        for line in self.buffer.splitlines():
            if not line.endswith("\n"): # stream not received entirely yet
                self.buffer = line
            parts = line.split()
            if parts[0].lower() == "p2p":
                action = int(parts.pop(2))
                version = parts.pop(1)
                parts.pop(0)
                args = parts
                action = ActionFactory.build_action(version, action, *args)
                self._actions.append(action)
            else:
                log.debug("Unknown header %s" % parts[0])

    def _pull_data(self):
        """Read the new data from the socket and store them in a buffer."""
        readable, w, e = select.select([self.socket], [], [],
                self._select_timeout)

        if len(readable) == 0:
            return False

        bufsize = 8192
        for sock in readable:
            data = sock.recv(bufsize)
            while True:
                self.buffer += data
                log.debug("RAW DATA FROM PEER: %s" % data)
                try:
                    data += sock.recv(bufsize)
                except socket.error:
                    # no more data to receive
                    break

        return True
