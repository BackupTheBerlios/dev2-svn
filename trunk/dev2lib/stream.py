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

"""Classes to create/decode streams.

A stream is a text representation of an action. XML streams are used in the
pair programming protocol.
"""

from dev2lib.action import ACTIONS
from dev2lib.errors import CouldNotBuildStreamForAction

class XMLStream:
    """XML representation of an action that can be sent across the network."""
    @classmethod
    def make_stream(klass, action):
        stream = u'<stream version="%d">%s</stream>'
        tree = klass._build_tree(action)
        stream = stream % (action.version, tree)

        return stream

    @classmethod
    def _build_tree(klass, action):
        tree = u""
        for attr in action.__dict__:
            dic = {'attr': attr, 'value': getattr(action, attr)}
            if dic['value'] != "":
                tree += u"<%(attr)s>%(value)s</%(attr)s>" % dic
            else:
                tree += u"<%(attr)s/>" % dic
        return tree


class TextStream:
    """Text representation of an action that can be sent across the nerwork."""
    stream = u'P2P %(version)d %(action)s'
    stream_start = stream + u' %(name)s'

    @classmethod
    def make_stream(klass, action):
        kw = klass._get_kw(action)
        if action.action in (ACTIONS['start'], ACTIONS['accept_start']):
            return klass.stream_start % kw
        raise CouldNotBuildStreamForAction(action.action)

    @classmethod
    def _build_start(klass, action):
        pass

    @classmethod
    def _get_kw(klass, action):
        kw = {}
        kw['version'] = action.version
        for attr in action.__dict__:
            kw[attr] = getattr(action, attr)

        return kw
