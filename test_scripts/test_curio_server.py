from curio.socket import *
from curio import run, spawn, tcp_server
import select
from UnityMeshByteHandler import debug

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
        self.client_sockets = {}
        self.write_time = []



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

    async def read_int(self, socket):
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
        # return await socket.recv(100)

    async def start_recv_mesh(self, socket, addr):
        '''
        :param socket:  
        :return: 
        1. get mesh size
            - 4 byte 
        2. Reply 'OK'
        3. get mesh
        '''
        print('Connection from', addr)
        data_size = await self.read_int(socket)
        await socket.send(str(data_size).encode())
        print("Mesh size: {}".format(data_size))


        # socket.close()
            # self.close_client_connection(socket)



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



    def run(self):
        print("Server running...")

        try:
            run(tcp_server, '', 11000, self.start_recv_mesh)
            # self.listen()
        except KeyboardInterrupt:
            pass
        finally:
            self.close()


if __name__ == '__main__':
    server = RemoteMeshTarget()
    server.run()