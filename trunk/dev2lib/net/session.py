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

"""TODO:

    Méthode qui contrôle l'arrivée de données sur la connexion. Probablement en
    utilisant le module select.

    Implémenter le système de vérouillage (lock).
    La méthode des sémaphores proposée par Mr Hyde a l'air vraiment
    intéressante mais peut-être trop dure à implémenter dans un premier temps.
    Peut-être, il serait plus simple, dans une première version, de donner la
    priorité au début de la session à l'utilisateur qui à initié la session
    (i.e. qui a démarré le serveur). Quand cet utilisateur aura dévérouillé le
    fichier l'autre pourra s'approprier les permissions de modification. et
    ainsi de suite.
"""

import logging
import socket
import sys
import threading

from dev2lib import event
from dev2lib.net import server, connection



log = logging.getLogger("dev2lib.net.session")
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s:" +
        " %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)


STATUS = {
    'connected': 1<<0,
    'not connected': 1<<1,
    'sending file': 1<<2,
    }

class Session:
    """Fournit les méthodes nécessaires pour interagir avec l'utilisateur
    distant.

    C'est une interface au-dessus de la couche réseau permettant la connexion
    à un utilisateur distant, l'attente de connexion, l'envoi de fichier, ...
    """
    def __init__(self, name="", addr=None, connection_handler=None):
        """
        Arguments:
            name -- nom de ce client
            connection_handler -- méthode qui sera appelée lorsqu'un
                utilisateur se sera connecté. C'est par exemple l'interface
                graphique qui fournira sa méthode pour qu'elle soit avertie en
                temps voulu.
        """
        log.debug("Initializing session")

        self.name = name
        self.addr = None
        self.server = None
        self.connection = None
        self.connection_handler = connection_handler
        self.event_handler = event.EventHandlerManager()
        self.status = STATUS['not connected']

    def listen(self, addr):
        """Start listening for pairs."""
        self.server = server.Server(self.handle_connection, addr)
        self.server.start()

    def connect(self, addr):
        """
        Arguments:
            addr -- tuple (host, port)
        """
        self.connection = connection.PairProgConnection()
        return self.connection.connect(addr)

    def close(self):
        """Terminer la session.

        Déconnexion de tous les socket et arrêt du serveur s'il est en route.
        """
        if self.connection is not None:
            self.connection.disconnect()
        if self.server is not None:
            self.server.close()

    def add_handler(self, cmd, callback):
        self.event_handler.add_handler(cmd, callback)

    def handle_connection(self, request, addr):
        """Traite une nouvelle connexion."""
        # Récupérer les infos nécessaires sur la connexion, venant de 
        # l'instance du serveur.
        self.connection = connection.PairProgConnection(socket=request)

        # Avertir de la nouvelle connexion, en passant une référence à cette
        # instance Session.
        self.connection_handler(self)

# METHODES DE SYNCHRONISATION DES FICHIERS

    def start(self, addr=None):
        """Start a new session."""
        assert (addr is None) and (self.addr is not None)
        if addr is not None:
            self.addr = addr

        if not self.connect(self.addr):
            return False

        action = ActionStart(self.name)
        stream = self.connection.send_stream(action)
