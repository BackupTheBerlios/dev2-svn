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

"""Classes to create actions for the pair programming protocol.

Actions in the pair programming protocol permit users to interact.
"""

from dev2lib.errors import UnknownAction
from dev2lib.protocol import Protocolv1

ACTIONS = {
    'start': 1,
    'accept_start': 2,
}

class ActionFactory:
    """Help build Action objects."""
    @classmethod
    def build_action(klass, version, actiontype, *args):
        """Construct an Action instance."""
        if actiontype == ACTIONS["start"]:
            name = ""
            if len(args) > 0:
                name = args[0]
            act = StartAction(name)
        elif actiontype == ACTIONS["accept_start"]:
            name = ""
            if len(args) > 0:
                name = args[0]
            act = AcceptStartAction(name)
        else:
            raise UnknownAction(actiontype)

        return act

class Action(Protocolv1):
    """All actions must derive from this one class."""
    def __init__(self, action):
        self.action = action

class StartAction(Action):
    """Request the beginning of pair programming session."""
    def __init__(self, name=""):
        self.name = name
        super(StartAction, self).__init__(ACTIONS['start'])

class AcceptStartAction(Action):
    """Accept the start request."""
    def __init__(self, name=""):
        self.name = name
        super(AcceptStartAction, self).__init__(ACTIONS['accept_start'])
