#!/usr/bin/env Python3

'''
MeshServer/MeshFlipHandler.py

'''

import os
import helper
import numpy


__author__ = "Seyoung Park"
__copyright__ = "Copyright 2017, Seyoung Park"
__credits__ = ["Seyoung Park"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Seyoung Park"
__email__ = "seyoung.arts.park@protonmail.com"
__status__ = "Production"

FILE = '/Users/young/CODE/MeshServer/concatenated/merged_obj_2.obj'

class ObjHeader:
    vertex = 'v '
    normals = 'vn'
    faces = 'f '
    def __init__(self, value):
        self.value = value


class MeshFlipHandler:

    def __init__(self):
        pass

    def is_vertice_line(self, line):
        return line[:2] == 'v '

    def get_digits_splitted_from_line(self, lines, header):
        return [l.split()[1:] for l in lines if l[:2] == header]

    def get_vertices(self, lines):
        vertices = self.get_digits_splitted_from_line(lines, 'v ')
        return numpy.array([ [ float(i) for i in line] for line in vertices])


    def read_faces(self, lines):
        lines = [l.split()[1:] for l in lines if l[:2] == 'f ']
        lines = [[int(i.split('//')[0]) for i in line] for line in lines]
        return numpy.array(lines)

    def normalize_v3(self, arr):
        ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
        lens = numpy.sqrt(arr[:, 0] ** 2 + arr[:, 1] ** 2 + arr[:, 2] ** 2)
        arr[:, 0] /= lens
        arr[:, 1] /= lens
        arr[:, 2] /= lens
        return arr

    def recalculate_normals(self, lines: list):
        """

        :type lines: object
        """
        faces = self.read_faces(lines)
        faces_for_norm = numpy.copy(faces) - 1
        # print(faces)
        vertices = self.get_vertices(lines)
        # print(vertices)

        norm = numpy.zeros(vertices.shape, dtype=vertices.dtype)
        # Create an indexed view into the vertex array using the array of three indices for triangles
        tris = vertices[faces_for_norm]
        # Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle
        n = numpy.cross(tris[::, 1] - tris[::, 0], tris[::, 2] - tris[::, 0])
        # n is now an array of normals per triangle. The length of each normal is dependent the vertices,
        # we need to normalize these, so that our next step weights each normal equally.
        self.normalize_v3(n)
        # now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
        # But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle,
        # the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to normalize again afterwards.
        # The cool part, we can actually add the normals through an indexed view of our (zeroed) per vertex normal array
        norm[faces_for_norm[:, 0]] += n
        norm[faces_for_norm[:, 1]] += n
        norm[faces_for_norm[:, 2]] += n

        norm = [ [str(l) for l in line] for line in norm]
        norm = ['vn ' + ' '.join(line) + '\n' for line in norm]
        return norm



    def flip(self, line):
        '''
        v 0.5355916023254395 -1.1006650924682617 3.853105306625366
        :param line: 
        :return: 
        '''
        elements = line.split()
        x = elements[1]
        x = '-' + x if x[0] != '-' else x[1:]
        elements[1] = x
        flipped_line = ' '.join(elements) + '\n'
        # print(line, flipped_line)
        return flipped_line

    def get_elements_as_list_of_strings(self, lines, header: ObjHeader):
        return [l for l in lines if l[:2] == header.value]


    def run(self):
        read_directory = 'objs/2017-05-17-Wed-13:58:25:196224'
        file_names = helper.get_filenames(read_directory)
        write_directory = read_directory + '_flipped/'
        if not os.path.exists(write_directory):
            os.makedirs(write_directory)


        for fn in file_names:
            with open(fn) as f:
                lines = f.readlines()
                lines = [self.flip(line) if self.is_vertice_line(line) else line for line in lines]
                normals = self.recalculate_normals(lines)

                vertices = self.get_elements_as_list_of_strings(lines, ObjHeader(ObjHeader.vertex))
                faces = self.get_elements_as_list_of_strings(lines, ObjHeader(ObjHeader.faces))

                # print(vertices)
                # print(normals)
                # print(faces)


                # with open("Flipped2.obj", 'w') as file:
                fn = os.path.basename(fn)
                with open(write_directory+fn, 'w') as file:
                    file.write('o Object.1\n')
                    file.writelines(vertices)
                    file.writelines(normals)
                    file.writelines(faces)


if __name__ == '__main__':
    mf = MeshFlipHandler()
    mf.run()