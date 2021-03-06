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

from dev2lib.action import ACTIONS


class EventHandlerManager:
    """Permet de lier une fonction � une commande sp�cifique ou � l'ensemble
    des commandes.
    """
    def __init__(self):
        # Les commandes sont stock�es dans un dictionnaire et elles ont pour
        # valeur la fonction qui leur est li�e.
        self.map = {}
        for numval in ACTIONS.values():
            self.map[numval] = None
        # Handler pour toutes les commandes.
        self.global_handler = None


    def set_global_handler(self, callback):
        """D�finit la m�thode qui sera appel�e � chaque commande re�ue.

        Arguments:
            callback -- m�thode ou fonction
        """
        self.global_handler = callback


    def remove_global_handler(self):
        """Met self.global_handler � None."""
        self.set_global_handler(None)


    def add_handler(self, action, callback):
        """D�finit une m�thode qui sera appel�e � chaque r�ception de la
        commande sp�cifi�e.

        Arguments:
            cmd -- numeric value of the command
            callback
        """
        if not action in self.map:
            return False

        self.map[action] = callback

        return True


    def handle(self, action):
        """Call the handler bound to the received command.

        Arguments:
            event -- an Event object, containing info on the event
        """
        if self.global_handler is not None:
            self.global_handler(action)

        if self.map[action.action] is not None:
            self.map[action.action](action)
