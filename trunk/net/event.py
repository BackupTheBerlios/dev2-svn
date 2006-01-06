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


"""
"""



import connection



class Event:
    """Stocke les infos sur une commmande de manière structurée et accessible.
    """
    def __init__(self, cmd, args=[]):
        self.cmd = cmd
        self.args = args



class EventHandlerManager:
    """Permet de lier une fonction à une commande spécifique ou à l'ensemble
    des commandes.
    """
    def __init__(self):
        # Les commandes sont stockées dans un dictionnaire et elles ont pour
        # valeur la fonction qui leur est liée.
        self.commands = {}
        for cmd in connection.commands:
            self.commands[cmd] = None
        # Handler pour toutes les commandes.
        self.global_handler = None


    def set_global_handler(self, callback):
        """Définit la méthode qui sera appelée à chaque commande reçue.

        Arguments:
            callback -- méthode ou fonction
        """
        self.global_handler = callback


    def remove_global_handler(self):
        """Met self.global_handler à None."""
        self.set_global_handler(None)


    def add_handler(self, cmd, callback):
        """Définit une méthode qui sera appelée à chaque réception de la
        commande spécifiée.

        Arguments:
            cmd -- nom de la commande
            callback -- méthode ou fonction
        """
        cmd = cmd.lower()
        if not cmd in self.commands.keys():
            return

        self.commands[cmd] = callback


    def handle(self, event):
        """Appel la méthode liée à la commande reçue.

        Arguments:
            event -- un object Event contenant les informations de la commande.
        """
        if self.global_handler is not None:
            self.global_handler(event)

        if self.commands[event.cmd()] is not None:
            self.commands[event.cmd()](event)
