import logging
import selectors
import socket
import struct

from operations import Operations

logging.basicConfig(filename='socket_server.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')


class Server(object):

    SERVER_ADDRESS = ('localhost', 10001)

    def __init__(self):
        """
        Server class constructor.
        """

        self.mysel = selectors.DefaultSelector()
        self.keep_running = True

    def read(self, connection):
        """
        It handles the callback for read events.

        :param connection: Socket of the incomming connection.
        :type connection: socket
        """

        client_address = connection.getpeername()
        logging.debug('read({})'.format(client_address))
        lengthbuf = self.recvall(connection, 4)

        try:
            length, = struct.unpack('!I', lengthbuf)
            data = self.recvall(connection, length)

        except TypeError:
            logging.debug('  closing')
            self.mysel.unregister(connection)
            connection.close()
            self.keep_running = False
            return

        if data:
            logging.debug('  received {!r}'.format(data))
            ops = Operations()
            result = ops.main(data)
            logging.debug('sent {!r}'.format(result))
            length = len(result)
            connection.sendall(struct.pack('!I', length))
            connection.sendall(result)

    def accept(self, sock):
        """
        It handles the callback for new connections.

        :param sock: Socket with the incomming connection.
        :type sock: socket
        """

        new_connection, addr = sock.accept()
        logging.debug('accept({})'.format(addr))
        self.mysel.register(new_connection, selectors.EVENT_READ, self.read)

    def recvall(self, sock, count):
        """
        It receives a complete message send through a socket and returns it.

        :param sock: Input socket.
        :type sock: socket
        :param count: Length of the incoming message.
        :type count: int
        :return: The message sent through the socket.
        :rtype: bytes
        """

        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def start(self):
        """
        It starts the socket server and sets it to listen.
        """

        logging.debug('starting up on {} port {}'.format(*self.SERVER_ADDRESS))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.SERVER_ADDRESS)
        server.listen(2)

        self.mysel.register(server, selectors.EVENT_READ, self.accept)

        while self.keep_running:
            for key, mask in self.mysel.select(timeout=1000):
                callback = key.data
                callback(key.fileobj)

        logging.debug('shutting down')
        self.mysel.close()
