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

import sys
import threading
from SocketServer import TCPServer



# D�finition d'exceptions sp�cifiques � ce module.
class Error(Exception):
    pass



class Server(TCPServer):
    """"""
    def __init__(self, connection_handler, addr):
        """
        Arguments:
            addr -- (host, port)
            connection_handler -- m�thode appell�e lorsqu'une connexion est
                �tablie, avec comme param�tres le socket et l'adresse du
                client.
        """
        TCPServer.__init__(self, addr, None)
        self.request_queue_size = 1 # 1 client par session max.
        self.connection_handler = connection_handler
        self.running = False
        self.threads = []


    def finish_request(self, request, addr):
        """Pr�vient d'une nouvelle connexion en appelant la m�thode fournie
        (connection_handler).

        D�marre un nouveau thread pour ne pas bloquer (c'est peut-�tre pas
        n�cessaire, faudra voir avec les tests).
        """
        t = threading.Thread(group=None, target=self.connection_handler,
                args=(request, addr))
        t.start()
        self.threads.append(t)


    def start(self):
        """D�marre le serveur dans un nouveau thread."""
        if not self.running:
            t = threading.Thread(target=self.handle_request)
            t.start()
            self.threads.append(t)


    def close(self):
        """Arr�t du serveur.

        Arr�t de tous les threads.
        """
        self.running = False
        for t in self.threads:
            t.join()
        self.server_close()



if __name__ == "__main__":
    try:
        server = Server()
        server.serve_forever()
    except KeyboardInterrrupt:
        sys.exit(0)