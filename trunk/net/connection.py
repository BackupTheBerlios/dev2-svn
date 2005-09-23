# -*- coding: iso-8859-1 -*-

# Dev2 a pair programming development tool
# Copyright (C) 2005 The Dev2 developoment team

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA


"""TODO:

    D�finir les commandes du protocole de pair-programming. Probablement
    ajouter le pr�fixe PAIR_ � chaque commande pour les distinguer de celles
    du futur protocole de chat.
"""



import socket



# Les commandes du protocole de pair programming.
commands = [
    "pair_hello",
    "pair_syncchar",
    "pair_sendfile",
    #...
]



class Connection:
    def __init__(self, socket=None):
        """
        Arguments:
            socket -- (optionel) un object socket valide
        """
        self.connected = False
        self.socket = socket
        if self.socket is not None:
            self.connected = True


    def connect(self, addr):
        """Connexion � un h�te distant.

        Arguments:
            addr -- tuple (host, port)
        """
        # Fermer une �ventuelle connexion �tablie auparavant.
        self.disconnect()

        # Cr�er un nouveau socket.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Essayer de se connecter.
            self.socket.connect(addr)
            self.connected = True
        except socket.error:
            # Connexion �chou�e.
            self.connected = False

        return self.is_connected()


    def disconnect(self):
        """Fermer la connexion."""
        if self.is_connected():
            try:
                self.socket.close()
            except socket.error:
                self.socket = None
            except:
                self.socket = None


    def is_connected(self):
        """Retourne True ou False en fonction de l'�tat de la connexion."""
        return self.connected


    def get_socket(self):
        return self.socket



class PairProgConnection(Connection):
    """Impl�mente les commandes de communication "pair-programming" avec le
    client.
    """
    def __init__(self, socket=None):
        Connection.__init__(self, socket=socket)


    def send(self, msg=[]):
        """Envoye une commande brute.

        Arguments:
            msg -- sequence contenant la commande suivie des param�tres
        """
        if not self.is_connected():
            return

        msg = " ".join(msg)
        return self.connection.send(msg)


    def hello(self, name):
        """EXAMPLE: La commande hello permet de donner son nom � l'autre
        utilisateur.
        """
        self.send(["PAIR_HELLO", name])


    def sync_char(self, param=[]):
        cmd = ["PAIR_SYNCCHAR"] + list(param)
        self.send(cmd)
