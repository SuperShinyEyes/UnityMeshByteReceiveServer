#!/usr/bin/env python3
import socket
import select


"""
Constants for commands.
"""
CLOSE_CMD='/close'      # Server shuts down
QUIT_CMD = '/quit'      # Client leaves
NICKNAME_CMD = '/nickname'
OK_MSG = 'OK'.encode()
ACCEPT_REPLY = '/accept'


'''
Debug constants
'''
DEBUG_MODE = True

def debug(msg):
    if DEBUG_MODE:
        print(msg)

class SessionSocket(object):
    """
    Pair of socket for one server-client session.
    """
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address[0]
        self.port = address[1]
        self.username = self.generate_username()

    def generate_username(self):
        import random
        random.seed()
        return "USER-{:d}".format(random.randint(1000000, 9999999))


class SampleServer(object):

    """IRC server."""
    def __init__(self, num_nodes=6, host='', host_ip='localhost', host_port=8888, timeout_in_sec=2):
        '''
        client_sockets = {client_socket: session_properties}
        client_sockets: Clients with username.
        client_sockets_before_join: Clients with random username. They need to
            enter their username in order to start a session.
        '''
        self.host = host
        self.host_port = host_port
        self.num_nodes = num_nodes
        self.socket = None
        self.client_sockets = {}
        self.init_socket_bind()
        self.username = "SERVER"
        self.listner_socket_timeout_in_sec = timeout_in_sec
        self.recv_mesh_timeout = 5



    def init_socket_bind(self):
        """
        Creates a socket.
        Reuse the same adress for the socket.
        Bind to a port.
        """
        self.socket = self.create_socket()
        print('Socket created')
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind()
        print('Socket now listening')
        self.socket.listen(self.num_nodes) # Defines how many sockets can be connected

    def create_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()

        return s

    def bind(self):
        #Bind socket to local host and port
        try:
            self.socket.bind((self.host, self.host_port))
        except socket.error as e:
            print('Bind failed. Error Code : ' + str(e[0]) + ' Message ' + e[1])
            sys.exit()
        else:
            print('Socket bind complete')

    def close_client_connection(self, client_socket, close_all=False):
        client_socket.close()

    def close_all_client_sockets(self, ):
        for client_socket in self.client_sockets.keys():
            self.close_client_connection(client_socket, True)

        self.client_sockets = {}

    def close(self):
        import time
        print("Closing....")
        self.close_all_client_sockets()
        self.socket.close()

    def add_client(self, session_socket):
        self.client_sockets[session_socket.socket] = session_socket


    def accept_client(self):
        print("New client")
        socket, address = self.socket.accept()

        '''
        Q. Do I need to set a socket as non-blocking?
        '''
        # Set socket to non-blocking mode.
        # Read "How to set timeout on python's socket recv method?":
        # http://stackoverflow.com/a/2721734/3067013
        # self.socket.setblocking(False)
        # speaker_socket.setblocking(False)
        print('Connected with ' + address[0] + ':' + str(address[1]))
        session_socket = SessionSocket(
            socket,
            address
        )
        self.add_client(session_socket)



    def recv_mesh_size(self, socket):
        '''
        
        :param socket: 
        :return: 
        '''
        data = socket.recv(40).decode()
        try:
            data = int(data)
        except ValueError as e:
            print(e)
            return -1
        else:
            return data

    def recv_mesh(self, socket, mesh_size):
        '''

        :param socket: 
        :return: 
        '''
        buffer = b''
        while len(buffer) < mesh_size:
            ready = select.select(
                [socket],
                [],
                [],
                self.recv_mesh_timeout
            )

            if not ready[0]:
                print("Time out")
                return -1

            buffer += socket.recv(1024)

        new_person = sample.Person()
        new_person.parse_from_bytes(buffer)
        print(new_person)
        return new_person

    def start_recv_mesh(self, socket):
        '''
        :param socket:  
        :return: 
        1. get mesh size
            - 4 byte 
        2. Reply 'OK'
        3. get mesh
        '''
        mesh_size = self.recv_mesh_size(socket)
        print("Mesh size: {}".format(mesh_size))
        if mesh_size < 0:
            return
        else:
            socket.sendall(OK_MSG)

        mesh = self.recv_mesh(socket, mesh_size)

    def listen(self):
        sockets = [self.socket]
        while True:

            '''
            According to Python3 doc:
            The return value is a triple of lists of objects that are ready:
            subsets of the first three arguments. When the time-out is reached
            without a file descriptor becoming ready, three empty lists are
            returned.
            '''

            ready = select.select(sockets + list(self.client_sockets.keys()), [], [], self.listner_socket_timeout_in_sec)
            #Receiving from client
            if not ready[0]:
                debug("No msg")
                continue

            socket = ready[0][0]
            if socket == self.socket:
                self.accept_client()

            else:
                debug("Got a msg")
                self.start_recv_mesh(socket)

    def run(self):
        print("Server running...")

        try:
            self.listen()
        except KeyboardInterrupt:
            pass
        finally:
            self.close()


def main():
    person = sample.Person()
    person.name = "S"
    encoded = person.encode_to_bytes()
    print(encoded)

if __name__ == '__main__':
    # main()
    server = SampleServer()
    server.run()