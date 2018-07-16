#!venv/bin python3


"""This is the preliminar backend."""
from socket import socket, AF_INET, SOCK_STREAM
from logging import getLogger, StreamHandler, Formatter, DEBUG, Logger
from threading import Thread
import sys

__author__ = 'Nicolas Quiroz'

fmt = Formatter('[%(name)s] %(message)s')
handler = StreamHandler(sys.stdout)
handler.setLevel(DEBUG)


class Server:
    """Server that handles every commands from the frontend."""

    def __init__(self, host='0', port='9999'):
        """
        Initialize the server.

        For simplificaton, server calls to the listening automatically
        """
        self.__alive = True
        self.port = port
        self.host = host
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.log: Logger = getLogger(f'Server {self.host}:{self.port}')
        self.log.setLevel(DEBUG)
        self.log.debug('Successfully initialized.')
        self.bind()
        self.listen()
        self.accept_conn()

    def bind(self):
        """Binds the current server to the respective host and port."""
        self.sock.bind((self.host, self.port))
        self.log.debug('Successfully bind.')

    def listen(self):
        """Beggins listening to bind address."""
        self.sock.listen()
        self.log.debug('Server is now listening.')

    def accept_conn(self):
        """Wait for the connection of the client."""
        self.cli_sock = self.sock.accept()
        while self.__alive:
            

