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


# Modules de la librairie standard.
import sys
import socket
import threading

# Modules internes à Dev².
import server
import connection
import event



class Session:
    """Fournit les méthodes nécessaires pour interagir avec l'utilisateur
    distant.

    C'est une interface au-dessus de la couche réseau permettant la connexion
    à un utilisateur distant, l'attente de connexion, l'envoi de fichier, ...
    """
    def __init__(self, name="", connection_handler=None):
        """
        Arguments:
            name -- nom de ce client
            connection_handler -- méthode qui sera appelée lorsqu'un
                utilisateur se sera connecté. C'est par exemple l'interface
                graphique qui fournira sa méthode pour qu'elle soit avertie en
                temps voulu.
        """
        self.name = name
        self.server = None
        self.connection = None
        self.connection_handler = connection_handler
        self.event_handler = event.EventHandlerManager()


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


    def wait_for_connection(self, addr):
        """Passe en mode attente de connexion d'un utilisateur distant.

        Démarre un serveur dans un autre thread qui appellera la méthode
        self.handle_connection quand un utilisateur se sera connecté.
        """
        if not hasattr("server", 'self'):
            self.server = server.Server(self.handle_connection, addr)
        self.server.start()


    def handle_connection(self, request, addr):
        """Traite une nouvelle connexion."""
        # Récupérer les infos nécessaires sur la connexion, venant de 
        # l'instance du serveur.
        self.connection = connection.PairProgConnection(socket=request)

        # Avertir de la nouvelle connexion, en passant une référence à cette
        # instance Session.
        self.connection_handler(self)


# METHODES DE SYNCHRONISATION DES FICHIERS

    def send_file(self, file_):
        """Envoyer un fichier pour travailler en paire dessus.

        Arguments:
            file -- référence à un objet fichier (i.e. qui dispose de la
                       méthode read()).
        """
        pass


    def sync_char(self, file_id, char, line, column):
        """Synchronise la chaîne de caractère 'char'.

        Arguments:
            file_id -- identifiant spécifique au fichier en cours de traitement
            char -- un caractère ou une chaîne de caractères
            line -- ligne dans laquelle se trouve le caractère
            column -- colonne dans laquelle se trouve le caractère
        """
        pass



if __name__ == "__main__":
    # Teste de la classe Session:

    def conn_handler(session):
        """Méthode qui sera appelée lors de la connexion d'un client."""
        print "new connection"

    addr = ("127.0.0.1", 9393)

    # Création d'une session.
    s1 = Session(connection_handler=conn_handler)
    # Prêt à recevoir la connexion d'un client.
    s1.wait_for_connection(addr)

    # Création d'une autre session.
    s2 = Session()
    # Connexion au premier client.
    s2.connect(addr)

    # Arrêt des sessions.
    s2.close()
    s1.close()

    # Force la fin du programme.
    sys.exit(0)
