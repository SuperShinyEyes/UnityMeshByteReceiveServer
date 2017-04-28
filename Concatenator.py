import os
import helper

READ_DIR_NAME = 'to_be_concatenated'
WRITE_DIR_NAME = 'concatenated'

class Concatenator:

    def __init__(self):
        self.lines = ''
        self.list_of_vertices_lists = []
        self.list_of_normals_list = []
        self.list_of_faces_list = []

    def get_vertices_as_list_of_strings(lines):
        return [l for l in lines if l[:2] == 'v ']

    def get_normals_as_list_of_strings(lines):
        return [l  for l in lines if l[:2] == 'vn']

    def get_faces_as_list_of_ints(lines):
        # l = f 1//1 3//3 9//9
        # lines = [ ["1//1", "3//3", "9//9"], .... ]
        lines = [l.split()[1:] for l in lines if l[:2] == 'f ']
        # lines = ["1//1", "3//3", "9//9", .... ]
        lines = list(itertools.chain.from_iterable(lines))
        # lines = ["1", "3", "9", .... ]
        lines = [l.split('//')[0] for l in lines]
        # lines = [1, 3, 9, .... ]
        lines = [int(i) for i in lines]
        return lines

    def read_obj(self, file_name):
        with open(fn) as f:
            # Remove header
            lines = f.readlines()[1:]
            vertices = self.get_vertices_as_list_of_strings(lines)
            normals = self.get_normals_as_list_of_strings(lines)
            faces = self.get_faces_as_list_of_ints(lines)

            self.list_of_vertices_lists.append(vertices)
            self.list_of_normals_list.append(normals)
            self.list_of_faces_list.append(faces)

    def update_faces(self):
        for i in range(1, len(self.list_of_faces_list)):
            # pad

    def run(self):
        file_names = helper.get_filenames(READ_DIR_NAME)
        for fn in file_names:
            self.read_obj(file_names)

        write_path = helper.get_target_path(WRITE_DIR_NAME)
        write_path = os.path.join(write_path, helper.get_random_name())
        with open(write_path, 'w') as f:
            f.write(self.lines)


if __name__ == '__main__':
    c = Concatenator()
    c.run()