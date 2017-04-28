from curio.socket import *
from curio import run, tcp_server
import select
from UnityMeshByteHandler import debug

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

class BufferOverRecvError(Exception):
    pass

class RemoteMeshTarget(object):

    def __init__(self, num_nodes=6, host='', host_ip='localhost', host_port=11000, timeout_in_sec=2):
        '''
        client_sockets = {client_socket: session_properties}
        client_sockets: Clients with username.
        client_sockets_before_join: Clients with random username. They need to
            enter their username in order to start a session.
        '''
        self.host = host
        self.host_port = host_port
        self.socket = None
        self.num_received_meshes = 0


    def close(self):
        print("Closing....")
        self.socket.close()


    async def read_data_size(self, socket):
        '''
        // The bytes arrive in the wrong order, so swap them.
        byte[] bytes = new byte[4];
        stream.Read(bytes, 0, 4);
        byte t = bytes[0];
        bytes[0] = bytes[3];
        bytes[3] = t;

        t = bytes[1];
        bytes[1] = bytes[2];
        bytes[2] = t;

        // Then bitconverter can read the int32.
        return BitConverter.ToInt32(bytes, 0);
        :param socket: 
        :return: 32 bit Int
        '''
        from struct import unpack
        read_size = 1
        byte_end = await socket.recv(read_size)
        byte_third = await socket.recv(read_size)
        byte_second = await socket.recv(read_size)
        byte_first = await socket.recv(read_size)
        bytes = byte_first + byte_second + byte_third + byte_end
        print("bytes: {} len: {}".format(bytes, len(bytes)))
        int32, = unpack('i', bytes)
        return int32

    def write_bytes(self, bytes, bytes_size_by_header):
        '''

        :param bytes_size_by_header: 
        :param meshes: 
        :return: 
        '''
        if len(bytes) != bytes_size_by_header:
            raise BufferOverRecvError

        from datetime import datetime
        import os
        time_format = '%Y-%m-%d-%a-%H:%M:%S:%f'
        filename = datetime.today().strftime(time_format)
        filepath = os.path.join('mesh_bytes', filename)
        with open(filepath, 'wb') as f:
            f.write(bytes)
        debug("Wrote {}".format(filepath))



    async def start_recv_mesh(self, socket, addr):
        '''
        :param socket:  
        :return: 
        1. get mesh size
            - 4 byte 
        2. Reply 'OK'
        3. get mesh
        '''

        data_size = await self.read_data_size(socket)
        data_buffer = b''
        self.num_received_meshes += 1
        print("#{}. Mesh size: {}".format(self.num_received_meshes, data_size))

        while len(data_buffer) < data_size:
            data_buffer += await socket.recv(data_size - len(data_buffer))

        try:
            self.write_bytes(data_buffer, data_size)
        except BufferOverRecvError as e:
            print(e, "Didn't receive enough")
        finally:
            socket.close()
            # self.close_client_connection(socket)



    def run(self):
        print("Server running...")

        try:
            run(tcp_server, '', 11000, self.start_recv_mesh)
            # self.listen()
        except KeyboardInterrupt:
            pass
        # finally:
            # self.close()


if __name__ == '__main__':
    server = RemoteMeshTarget()
    server.run()