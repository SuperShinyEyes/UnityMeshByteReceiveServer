#!/usr/bin/env python3

from struct import unpack
import UnityMeshObjectModel
import io
import numpy

class EmptyByteError(Exception):
    pass


'''
Debug constants
'''
DEBUG_MODE = True


def debug(msg):
    if DEBUG_MODE:
        print(msg)
class UnityMeshByteHandler(object):
    def __init__(self):
        self.reader_pos = 0
        self.meshes = []
        # Two c# Int32: 4 * 2 = 8
        self.header_size = 8
        self.reader_pos = 0

    def is_empty_byte(self, data):
        return len(data) == 0

    def get_stream_size(self, stream: io.TextIOWrapper):
        stream_len = stream.seek(0, 2)
        stream.seek(0, 0)
        return stream_len

    def deserialize(self, stream):
        '''
        :param stream: byte 
        :return: 
        '''
        meshes = []
        stream_len = self.get_stream_size(stream)
        debug("stream_len: {}".format(stream_len))
        while stream_len - self.reader_pos >= self.header_size:
            meshes.append(self.read_mesh(stream))
        self.write_meshes(meshes)

    def write_meshes(self, meshes):
        '''

        :param meshes: 
        :return: 
        '''
        from datetime import datetime
        import os
        time_format = '%Y-%m-%d-%a-%H:%M:%S'
        filename = datetime.today().strftime(time_format) + '.obj'
        filepath = os.path.join('objs', filename)
        with open(filepath, 'w') as f:

            for i in range(len(meshes)):
                self.write_mesh(f, meshes[i], i+1)

    def write_mesh(self, stream: io.TextIOWrapper, mesh: UnityMeshObjectModel.Mesh, index):
        header = 'o Object.{}\n'.format(index)
        stream.write(header)

        # for v in mesh.vertices:
        #     line = "v {x} {y} {z}".format(x=v.x, y=v.y, z=v.z)

        lines = ["v {x} {y} {z}\n".format(x=v[0], y=v[1], z=v[2]) for v in mesh.vertices]
        stream.writelines(lines)
        stream.write("\n\n")

        lines = ["vn {x} {y} {z}\n".format(x=v[0], y=v[1], z=v[2]) for v in mesh.norm]
        stream.writelines(lines)
        stream.write("\n\n")

        lines = ["f {x}//{x} {y}//{y} {z}//{z}\n".format(x=v[0], y=v[1], z=v[2]) for v in mesh.faces]
        stream.writelines(lines)
        stream.write("\n\n")
        debug(mesh.faces)


    def read_mesh(self, stream):

        vertex_count, triangle_index_count = self.read_mesh_header(stream)
        vertices = self.read_vertices(stream, vertex_count)
        # triangle_indicies = self.read_triangle_indicies(stream, triangle_index_count)


        faces = self.read_faces(stream, triangle_index_count)
        # Create a zeroed array with the same type and shape as our vertices i.e., per vertex normal
        norm = numpy.zeros(vertices.shape, dtype=vertices.dtype)
        # Create an indexed view into the vertex array using the array of three indices for triangles
        tris = vertices[faces]
        # Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle
        n = numpy.cross(tris[::, 1] - tris[::, 0], tris[::, 2] - tris[::, 0])
        # n is now an array of normals per triangle. The length of each normal is dependent the vertices,
        # we need to normalize these, so that our next step weights each normal equally.
        self.normalize_v3(n)
        # now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
        # But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle,
        # the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to normalize again afterwards.
        # The cool part, we can actually add the normals through an indexed view of our (zeroed) per vertex normal array
        norm[faces[:, 0]] += n
        norm[faces[:, 1]] += n
        norm[faces[:, 2]] += n

        mesh = UnityMeshObjectModel.Mesh(vertices, faces, norm)
        return mesh

    def read_mesh_header(self, stream) -> object:
        '''
        :param stream: 
        :return: 
        '''
        vertex_count = self.read_int32(stream)
        triangleIndexCount = self.read_int32(stream)
        debug('vertex_count: {}\ttriangleIndexCount: {}'.format(vertex_count , triangleIndexCount))
        return vertex_count, triangleIndexCount

    def read_vertices(self, stream, vertexCount):
        '''
        Vector3[] vertices = new Vector3[vertexCount];
        :param vertexCount: 
        :param stream: 
        :return: 
        '''
        # vertices = [
        #     UnityMeshObjectModel.Vector3(
        #         self.read_single(stream),
        #         self.read_single(stream),
        #         self.read_single(stream)
        #     ) for _ in range(vertexCount)
        # ]
        vertices = numpy.array([
            [
                self.read_single(stream),
                self.read_single(stream),
                self.read_single(stream)
            ] for _ in range(vertexCount)
        ])
        return vertices

    def read_faces(self, stream, triangleIndexCount):
        '''
        Vector3[] vertices = new Vector3[vertexCount];
        :param triangleIndexCount: 
        :param stream: 
        :return: 
        '''
        faces = numpy.array([
            [
                self.read_int32(stream),
                self.read_int32(stream),
                self.read_int32(stream)
            ]
            for _ in range(triangleIndexCount//3)
        ])
        return faces

    def read_triangle_indicies(self, stream, triangleIndexCount):
        '''
        Vector3[] vertices = new Vector3[vertexCount];
        :param triangleIndexCount: 
        :param stream: 
        :return: 
        '''
        triangleIndicies = [
            self.read_int32(stream) for _ in range(triangleIndexCount)
        ]
        return triangleIndicies

    def normalize_v3(self, arr):
        ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
        lens = numpy.sqrt(arr[:, 0] ** 2 + arr[:, 1] ** 2 + arr[:, 2] ** 2)
        arr[:, 0] /= lens
        arr[:, 1] /= lens
        arr[:, 2] /= lens
        return arr

    def read_int32(self, stream):
        '''
        Read 4 byte from data
        :param stream: 
        :return: truncated data and int
        '''
        # if is_empty_byte(data):
        #     raise EmptyByteError
        # print(type(stream))
        foo = stream.read(4)
        # print(foo, type(foo))

        # return "foo"
        int32, = unpack('i', foo)
        self.reader_pos += 4
        return int32

    def read_single(self, stream: io.TextIOWrapper):
        '''
        Read 4 byte from data
        :param stream: 
        :return: truncated data and int
        '''
        # if is_empty_byte(data):
        #     raise EmptyByteError
        # print(type(stream))
        foo = stream.read(4)
        # print(stream.tell(), foo, type(foo))

        # return "foo"
        single, = unpack('f', foo)
        self.reader_pos += 4
        return single

    def run(self):
        with open('bytes/5_34_00 PM.room', 'rb') as f:
            self.deserialize(f)