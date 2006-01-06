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

    M�thode qui contr�le l'arriv�e de donn�es sur la connexion. Probablement en
    utilisant le module select.

    Impl�menter le syst�me de v�rouillage (lock).
    La m�thode des s�maphores propos�e par Mr Hyde a l'air vraiment
    int�ressante mais peut-�tre trop dure � impl�menter dans un premier temps.
    Peut-�tre, il serait plus simple, dans une premi�re version, de donner la
    priorit� au d�but de la session � l'utilisateur qui � initi� la session
    (i.e. qui a d�marr� le serveur). Quand cet utilisateur aura d�v�rouill� le
    fichier l'autre pourra s'approprier les permissions de modification. et
    ainsi de suite.
"""


# Modules de la librairie standard.
import sys
import socket
import threading
import logging

# Modules internes � Dev�.
import server
import connection
import event



log = logging.getLogger("net.session")
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s:" +
        " %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)
log.debug("test")


class Session:
    """Fournit les m�thodes n�cessaires pour interagir avec l'utilisateur
    distant.

    C'est une interface au-dessus de la couche r�seau permettant la connexion
    � un utilisateur distant, l'attente de connexion, l'envoi de fichier, ...
    """
    def __init__(self, name="", connection_handler=None):
        """
        Arguments:
            name -- nom de ce client
            connection_handler -- m�thode qui sera appel�e lorsqu'un
                utilisateur se sera connect�. C'est par exemple l'interface
                graphique qui fournira sa m�thode pour qu'elle soit avertie en
                temps voulu.
        """
        log.debug("Initializing session")

        self.name = name
        self.server = None
        self.connection = None
        self.connection_handler = connection_handler
        self.event_handler = event.EventHandlerManager()

        log.debug("Session initialized")


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

        D�connexion de tous les socket et arr�t du serveur s'il est en route.
        """
        if self.connection is not None:
            self.connection.disconnect()
        if self.server is not None:
            self.server.close()


    def add_handler(self, cmd, callback):
        self.event_handler.add_handler(cmd, callback)


    def handle_connection(self, request, addr):
        """Traite une nouvelle connexion."""
        # R�cup�rer les infos n�cessaires sur la connexion, venant de 
        # l'instance du serveur.
        self.connection = connection.PairProgConnection(socket=request)

        # Avertir de la nouvelle connexion, en passant une r�f�rence � cette
        # instance Session.
        self.connection_handler(self)


# METHODES DE SYNCHRONISATION DES FICHIERS

    def send_file(self, file_):
        """Envoyer un fichier pour travailler en paire dessus.

        Arguments:
            file -- r�f�rence � un objet fichier (i.e. qui dispose de la
                       m�thode read()).
        """
        pass


    def sync_char(self, file_id, char, line, column):
        """Synchronise la cha�ne de caract�re 'char'.

        Arguments:
            file_id -- identifiant sp�cifique au fichier en cours de traitement
            char -- un caract�re ou une cha�ne de caract�res
            line -- ligne dans laquelle se trouve le caract�re
            column -- colonne dans laquelle se trouve le caract�re
        """
        pass



if __name__ == "__main__":
    # Teste de la classe Session:

    def conn_handler(session):
        """M�thode qui sera appel�e lors de la connexion d'un client."""
        print "new connection"

    addr = ("127.0.0.1", 9393)

    # Cr�ation d'une session.
    s1 = Session(connection_handler=conn_handler)
    s1.listen(addr)

    # Cr�ation d'une autre session.
    s2 = Session()
    # Connexion au premier client.
    s2.connect(addr)

    # Arr�t des sessions.
    s2.close()
    s1.close()

    # Force la fin du programme.
    sys.exit(0)
