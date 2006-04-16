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

import logging
import sys
import threading
from SocketServer import TCPServer



log = logging.getLogger("dev2lib.net.server")
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s:" +
        " %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)



class Server(TCPServer):
    """"""
    def __init__(self, connection_handler, addr):
        """
        Arguments:
            addr -- (host, port)
            connection_handler -- méthode appellée lorsqu'une connexion est
                établie, avec comme paramètres le socket et l'adresse du
                client.
        """
        TCPServer.__init__(self, addr, None)
        self.request_queue_size = 1 # max 1 client per session
        self.connection_handler = connection_handler
        self.running = False
        self.threads = []

    def finish_request(self, request, addr):
        """Prévient d'une nouvelle connexion en appelant la méthode fournie
        (connection_handler).

        Démarre un nouveau thread pour ne pas bloquer (c'est peut-être pas
        nécessaire, faudra voir avec les tests).
        """
        log.info("New client from %s on port %d" % addr)
        log.debug(request.getpeername())
        t = threading.Thread(group=None, target=self.connection_handler,
                args=(request, addr))
#        t.start()
#        self.threads.append(t)
        self.connection_handler(request, addr)

    def close_request(self, request):
        pass

    def handle_request_thread(self):
        """Démarre le serveur dans un nouveau thread."""
        if not self.running:
            log.info("Listening on %s on port %d" % self.server_address)
            t = threading.Thread(target=self.handle_request)
            t.start()
            self.threads.append(t)
        else:
            log.warning("Server already running")


    def close(self):
        """Arrêt du serveur.

        Arrêt de tous les threads.
        """
        if not self.running:
            return
        log.info("Shutting down server")
        self.running = False
        for t in self.threads:
            t.join()
        self.server_close()



if __name__ == "__main__":
    addr = ("127.0.0.1", 12345)
    try:
        server = Server(None, addr)
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
