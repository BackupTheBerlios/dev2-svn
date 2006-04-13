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



import dev2lib.net.connection as connection



class Event:
    """Store info on an event."""
    def __init__(self, action):
        self.action = action



class EventHandlerManager:
    """Permet de lier une fonction à une commande spécifique ou à l'ensemble
    des commandes.
    """
    def __init__(self):
        # Les commandes sont stockées dans un dictionnaire et elles ont pour
        # valeur la fonction qui leur est liée.
        self.commands = {}
        for cmd in connection.commands:
            numval = connection.commands[cmd]
            self.commands[numval] = None
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
            cmd -- numeric value of the command
            callback
        """
        if not cmd in self.commands:
            return

        self.commands[cmd] = callback


    def handle(self, event):
        """Call the handler bound to the received command.

        Arguments:
            event -- an Event object, containing info on the event
        """
        if self.global_handler is not None:
            self.global_handler(event)

        if self.commands[event.cmd] is not None:
            self.commands[event.cmd](event)
