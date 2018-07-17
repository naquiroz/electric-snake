#!venv/bin python3


"""This is the preliminar backend."""
from socket import socket, AF_INET, SOCK_STREAM
from logging import getLogger, StreamHandler, Formatter, DEBUG, Logger
from threading import Thread, Event
import json
import sys

__author__ = 'Nicolas Quiroz'

fmt = Formatter('[%(name)s] %(message)s')
handler = StreamHandler(sys.stdout)
handler.setFormatter(fmt)
handler.setLevel(DEBUG)


class Server:
    """Server that handles every commands from the frontend."""

    def __init__(self, host='0', port=9999):
        """
        Initialize the server.

        For simplificaton, server calls to the listening automatically
        """
        self.__killed = Event()
        self.port = port
        self.host = host
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.log: Logger = getLogger(f'Server {self.host}:{self.port}')
        self.log.setLevel(DEBUG)
        self.log.addHandler(handler)
        self.log.debug('Successfully initialized.')
        self.bind()
        self.listen()
        self.accept_conn()

    @property
    def alive(self):
        """Return if the server is running or not."""
        return not self.__killed.is_set

    def kill(self):
        """Kill the server signal."""
        self.__killed.set()

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
        close_thread = Thread(target=self.close_thread, name='Main')
        close_thread.start()
        cli_sock, _ = self.sock.accept()
        cli_thread = Thread(target=self.listen_cli,
                            args=(cli_sock, ), daemon=True)
        cli_thread.start()

    def close_thread(self):
        """Listen to signal of close, and consequently close."""
        self.__killed.wait()
        self.log.debug('Closing server...')
        self.sock.close()
        self.log.debug('Server is now closed.')
        exit()

    def listen_cli(self, cli_sock: socket):
        """Begin listening the client, until the server gets closed."""
        self.log.debug(f'Server is now listening to {cli_sock.getsockname}')
        while True:
            chunk_size_in_bytes = cli_sock.recv(4)
            self.log.debug('Server has received a new command, downloading...')
            chunk_size = int.from_bytes(chunk_size_in_bytes, byteorder='big')
            response = bytearray()
            while len(response) < chunk_size:
                read_size = min(4096, chunk_size - len(response))
                response.extend(cli_sock.recv(read_size))
            received = response.decode(encoding='utf-8')
            self.log.debug(f'Download finished. Response: {repr(received)}')
            if isinstance(received, str) and received:
                response = self.handle_command(received, cli_sock)
                if not self.__killed.is_set:
                    self.send(response, cli_sock)

    def handle_command(self, received_str: str, client_socket: socket):
        """Handle the command string received from the client socket."""
        cmd_json: dict = json.loads(received_str)
        cmd = cmd_json['command']
        if cmd == 'login':
            return {'status': 'success', 'response': {'authorized': True}}
        elif cmd == 'kill':
            self.log.debug('Killing server..')
            self.kill()
        else:
            return {'status': 'failed', 'reason': 'Unknown internal error'}

    def send(self, response_dict: dict, client_socket: socket):
        """Send the response to the client socket."""
        self.log.debug(f'Sending response: {repr(response_dict)}')
        response: bytes = json.dumps(response_dict).encode()

        length = len(response).to_bytes(4, byteorder='big')
        client_socket.send(length + response)
        self.log.debug('Response sent.')


if __name__ == "__main__":
    server = Server()
