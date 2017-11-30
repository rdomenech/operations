#!/usr/bin/python

import logging
import selectors
import socket
import struct

logging.basicConfig(filename='socket_client.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')

outgoing = []


def recvall(sock, count):
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


def get_data():
    """
    It reads the operations from a file and store them in a list.
    """

    with open('operations.txt', 'rb') as f:
        for line in f:
            outgoing.append(line.strip())


def put_data(data):
    """
    It writes the results in a file.
    :param data: Result of an operation.
    :type data: str
    """

    with open('results.txt', 'a') as f:
        f.write('{}\n'.format(data))


def connect():
    """
    It creates a socket object, connects it to the socket server and returns
    the socket.

    :return: The socket connected to the socket server.
    :rtype: socket.socket
    """

    server_address = ('localhost', 10001)
    logging.debug('connecting to {} port {}'.format(*server_address))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    return sock


def read(connection, number_msgs_received):
    """
    It reads the response from the server and updates the counter of messages
    received.

    :param connection:
    :param number_msgs_received: Number of messages received.
    :type number_msgs_received: int
    :return: Number of messages received.
    :rtype: int
    """

    logging.debug('  ready to read')
    lengthbuf = recvall(connection, 4)
    length, = struct.unpack('!I', lengthbuf)
    data = recvall(connection, length)

    if data:
        number_msgs_received += 1
        logging.debug('  received {!r}'.format(data))
        put_data(data.decode('utf-8'))

    return number_msgs_received


def write(mysel, sock, number_msgs_sent):
    """
    It sends the message to the socket server, updates the counter of
    messages sent and returns it.

    :param mysel: EpollSelector instance.
    :type mysel: selectors.EpollSelector
    :param sock: Socket connection to the server socket.
    :type sock: socket.socket
    :param number_msgs_sent: Counter of messages sent.
    :type number_msgs_sent: int
    :return: Counter of messages sent.
    :rtype: int
    """

    logging.debug('  ready to write')
    if not outgoing:
        logging.debug('  switching to read-only')
        mysel.modify(sock, selectors.EVENT_READ)
    else:
        number_msgs_sent += 1
        # Send the next message.
        next_msg = outgoing.pop()
        length = len(next_msg)
        logging.debug('  sending {!r}'.format(next_msg))
        sock.sendall(struct.pack('!I', length))
        sock.sendall(next_msg)

    return number_msgs_sent


def close(mysel, connection):
    """
    It closes the connection between the socket client and the socket server.

    :param mysel: EpollSelector instance.
    :type mysel: selectors.EpollSelector
    :param connection: File object associated to the connection.
    :type connection: file
    """

    logging.debug('shutting down')
    mysel.unregister(connection)
    connection.close()
    mysel.close()


def main():
    """
    Main method of the client. It starts the connection with the socket
    server, sends all the data and closes the connection when it got all the
    responses.
    """

    mysel = selectors.DefaultSelector()
    keep_running = True
    number_msgs_sent = 0
    number_msgs_received = 0
    get_data()
    sock = connect()
    mysel.register(
        sock,
        selectors.EVENT_READ | selectors.EVENT_WRITE,
    )

    while keep_running:
        logging.debug('starting up')
        for key, mask in mysel.select():
            connection = key.fileobj
            client_address = connection.getpeername()
            logging.debug('client({})'.format(client_address))

            if mask & selectors.EVENT_READ:
                number_msgs_received = read(connection, number_msgs_received)

            if mask & selectors.EVENT_WRITE:
                number_msgs_sent = write(mysel, sock, number_msgs_sent)

            keep_running = (not number_msgs_sent == number_msgs_received)

    close(mysel, connection)


if __name__ == "__main__":
    main()
