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

"""Define dev2lib specific exceptions."""

class Error(Exception):
    """Error"""
    def __str__(self):
        return self.__doc__ % self.__dict__


class CouldNotBuildStream(Error):
    """Could not build stream"""
    pass

class CouldNotBuildStreamForAction(CouldNotBuildStream):
    """Action %(action)s not supported"""
    def __init__(self, action):
        self.action = action


class UnknownAction(Error):
    """Unknown action %(action)s"""
    def __init__(self, action):
        self.action
