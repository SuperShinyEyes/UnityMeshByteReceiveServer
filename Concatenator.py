import os
import helper
import numpy

READ_DIR_NAME = 'to_be_concatenated'
WRITE_DIR_NAME = 'concatenated'


class ObjMesh:

    def __init__(self, index, v, n, f):
        self.index = index
        self.v = v
        self.n = n
        self.f = f


class Concatenator:

    def __init__(self):
        self.lines = ''
        self.obj_meshes = []
        self.index_to_be_padded_to_faces = 0
        self.list_of_vertices_lists = []
        self.list_of_normals_list = []
        self.list_of_faces_list = []
        self.target_write_file_name = self.get_target_write_file_name()

    def get_vertices_as_list_of_strings(self, lines):
        return [l for l in lines if l[:2] == 'v ']

    def get_normals_as_list_of_strings(self, lines):
        return [l  for l in lines if l[:2] == 'vn']

    def get_faces_as_list_of_ints(self, lines: list):
        # l = f 1//1 3//3 9//9
        # lines = [ ["1//1", "3//3", "9//9"], .... ]
        lines = [l.split()[1:] for l in lines if l[:2] == 'f ']
        # lines = [[1, 3, 9], .... ]
        lines = [[int(i.split('//')[0]) + self.index_to_be_padded_to_faces for i in line] for line in lines]

        lines = [['{}//{}'.format(i, i) for i in line] for line in lines]

        lines = ['f ' + ' '.join(line) + "\n" for line in lines]
        # print(lines)


        # # lines = ["1//1", "3//3", "9//9", .... ]
        # lines = list(itertools.chain.from_iterable(lines))
        # # lines = ["1", "3", "9", .... ]
        # lines = [l.split('//')[0] for l in lines]
        # # lines = [1, 3, 9, .... ]
        # lines = [int(i) + self.index_to_be_padded_to_faces for i in lines]
        #
        # lines =

        return lines

    def get_target_write_file_name(self):
        file_names = helper.get_filenames(WRITE_DIR_NAME)
        name = WRITE_DIR_NAME + "/merged_obj_{}.obj".format(len(file_names) + 1)
        print("Write on ", name)
        return WRITE_DIR_NAME + "/merged_obj_{}.obj".format(len(file_names) + 1)

    def concatenate(self, header: str, v: list, n:list, f:list, file_name=None):
        if not file_name:
            file_name = self.target_write_file_name
        with open(file_name, 'a') as file:
            file.write(header)
            file.writelines(v)
            file.writelines(n)
            file.writelines(f)

    def read_obj(self, file_name, i=1):
        with open(file_name) as f:
            # Remove header
            header = "\no Object.{}\n".format(i)
            lines = f.readlines()


            vertices = self.get_vertices_as_list_of_strings(lines)
            normals = self.get_normals_as_list_of_strings(lines)

            faces = self.get_faces_as_list_of_ints(lines)

            self.concatenate(header, vertices, normals, faces)
            # mesh = ObjMesh(self, i, vertices, normals, faces)
            # self.list_of_vertices_lists.append(vertices)
            # self.list_of_normals_list.append(normals)
            # self.list_of_faces_list.append(faces)

            # self.obj_meshes.append(mesh)


            # Finally
            self.index_to_be_padded_to_faces += len(vertices)

    # def update_faces(self):
    #     for i in range(1, len(self.list_of_faces_list)):
    #         # pad

    def run(self):
        file_names = helper.get_filenames(READ_DIR_NAME)
        for i in range(len(file_names)):
        # for fn in file_names:
            self.read_obj(file_names[i], i+1)

        # write_path = helper.get_target_path(WRITE_DIR_NAME)
        # write_path = os.path.join(write_path, helper.get_random_name())
        # with open(write_path, 'w') as f:
        #     f.write(self.lines)


if __name__ == '__main__':
    c = Concatenator()
    c.run()


# class Concatenator:
#
#     def __init__(self):
#         self.lines = ''
#         self.obj_meshes = []
#         self.index_to_be_padded_to_faces = 0
#         self.list_of_vertices_lists = []
#         self.list_of_normals_list = []
#         self.list_of_faces_list = []
#         self.target_write_file_name = self.get_target_write_file_name()
#
#     def get_target_write_file_name(self):
#         file_names = helper.get_filenames(WRITE_DIR_NAME)
#         return WRITE_DIR_NAME + "/merged_obj_{}.obj".format(len(file_names) + 1)
#
#
#     def get_faces_as_list_of_ints(lines):
#         # l = f 1//1 3//3 9//9
#         # lines = [ ["1//1", "3//3", "9//9"], .... ]
#         lines = [l.split()[1:] for l in lines if l[:2] == 'f ']
#         # lines = ["1//1", "3//3", "9//9", .... ]
#         lines = list(itertools.chain.from_iterable(lines))
#         # lines = ["1", "3", "9", .... ]
#         lines = [l.split('//')[0] for l in lines]
#         # lines = [1, 3, 9, .... ]
#         lines = [int(i) for i in lines]
#         return lines
#
#     def concatenate(self, lines: list, file_name="merged"):
#         with open(self.target_write_file_name, 'a') as f:
#             f.writelines(lines)
#
#     def read_obj(self, file_name, i=1):
#         with open(file_name) as f:
#             header = "\no Object.{}\n".format(i)
#             lines = f.readlines()
#             lines[0] = header
#             self.concatenate(lines)
#
#
#
#     def update_faces(self):
#         for i in range(1, len(self.list_of_faces_list)):
#             pass
#
#     def run(self):
#         file_names = helper.get_filenames(READ_DIR_NAME)
#         for i in range(len(file_names)):
#         # for fn in file_names:
#             self.read_obj(file_names[i], i+1)
#
#         # write_path = helper.get_target_path(WRITE_DIR_NAME)
#         # write_path = os.path.join(write_path, helper.get_random_name())
#         # with open(write_path, 'w') as f:
#         #     f.write(self.lines)