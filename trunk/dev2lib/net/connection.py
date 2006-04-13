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

import socket
import logging



log = logging.getLogger("net.connection")
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s:" +
        " %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)



commands = {
    "p2p_init": 100,
    "p2p_syncchar": 101,
    "p2p_sendfile": 102,
}


class Connection:
    def __init__(self, socket=None):
        """
        Arguments:
            socket -- (optionel) un object socket valide
        """
        log.info("Initializing connection")

        self.connected = False
        self.socket = socket
        if self.socket is not None:
            # XXX An improvement would be to check the validity of the socket.
            self.connected = True


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
            self.connected = True
        except socket.error:
            log.exception("Connection failed")
            # Connexion échouée.
            self.connected = False

        return self.is_connected()


    def disconnect(self):
        """Fermer la connexion."""
        if self.is_connected():
            try:
                log.info("Disconnecting...")
                self.socket.close()
            except socket.error:
                log.warning("Error while disconnecting")
                self.socket = None
            except:
                log.warning("Error while disconnecting")
                self.socket = None


    def is_connected(self):
        """Retourne True ou False en fonction de l'état de la connexion."""
        return self.connected


    def get_socket(self):
        return self.socket



class PairProgConnection(Connection):
    """Implémente les commandes de communication "pair-programming" avec le
    client.
    """
    def __init__(self, socket=None):
        Connection.__init__(self, socket=socket)


    def send(self, msg=[]):
        """Envoye une commande brute.

        Arguments:
            msg -- sequence contenant la commande suivie des paramètres
        """
        if not self.is_connected():
            return

        msg = " ".join(msg)
        log.debug("TO SERVER: %s" % msg)
        return self.connection.send(msg)


    def init(self, name):
        """Initialize the pair programming session.

        Inform the server of our name.
        """
        cmd = commands["p2p_init"]
        self.send([cmd, name])


    def sync_char(self, param=[]):
        cmd_code = command["p2p_sync_char"]
        cmd = [cmd_code] + list(param)
        self.send(cmd)
