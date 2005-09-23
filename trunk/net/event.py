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
"""



import connection



class Event:
    """Stocke les infos sur une commmande de mani�re structur�e et accessible.
    """
    def __init__(self, cmd, args=[]):
        self._cmd = cmd
        self._args = args

    def cmd(self):
        return self._cmd

    def args(self):
        return self._args



class EventHandlerManager:
    """Permet de lier une fonction � une commande sp�cifique ou � l'ensemble
    des commandes.
    """
    def __init__(self):
        # Les commandes sont stock�es dans un dictionnaire et elles ont pour
        # valeur la fonction qui leur est li�e.
        self.commands = {}
        for cmd in connection.commands:
            self.commands[cmd] = None
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


    def add_handler(self, cmd, callback):
        """D�finit une m�thode qui sera appel�e � chaque r�ception de la
        commande sp�cifi�e.

        Arguments:
            cmd -- nom de la commande
            callback -- m�thode ou fonction
        """
        cmd = cmd.lower()
        if not cmd in self.commands.keys():
            return

        self.commands[cmd] = callback


    def handle(self, event):
        """Appel la m�thode li�e � la commande re�ue.

        Arguments:
            event -- un object Event contenant les informations de la commande.
        """
        if self.global_handler is not None:
            self.global_handler(event)

        if self.commands[event.cmd()] is not None:
            self.commands[event.cmd()](event)
