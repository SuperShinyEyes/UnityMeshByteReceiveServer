import unittest
import os
import itertools

class ListsLengthNotEqualError(Exception):
    pass

def get_mesh_file_lines(dir_name):
    # dir_name = 'unittest_objs_reference/'
    all_file_names = os.listdir(dir_name)
    mesh_file_name = [i for i in all_file_names if i[-3:] == "obj"][0]
    mesh_file_path = os.path.join(dir_name, mesh_file_name)
    with open(mesh_file_path) as f:
        return f.readlines()

def get_vertices_received():
    lines = get_mesh_file_lines('unittest_objs_received/')
    lines = [l.split()[1:] for l in lines if l[:2] == 'v ']
    lines = list(itertools.chain.from_iterable(lines))
    lines = [float(i[:9]) for i in lines]
    return lines


def get_vertices_reference():
    lines = get_mesh_file_lines('unittest_objs_reference/')
    lines = lines[:lines.index("ppp\n")]
    lines = [l.split() for l in lines]
    lines = list(itertools.chain.from_iterable(lines))
    lines = [float(i) for i in lines]
    return lines


def get_faces_received():
    lines = get_mesh_file_lines('unittest_objs_received/')
    lines = [l.split()[1:] for l in lines if l[:2] == 'f ']
    lines = list(itertools.chain.from_iterable(lines))
    lines = [l.split('//')[0] for l in lines]
    lines = [int(i) for i in lines]
    return lines


def is_almost_equal(l1, l2, epsilon=0.00001):
    if len(l1) != len(l2):
        raise ListsLengthNotEqualError
    for i in range(len(l1)):
        if abs(l1[i] - l2[i]) > epsilon:
            print("index: ", i, l1[i], l2[i])
            return False
    else:
        return True


def get_faces_reference():
    lines = get_mesh_file_lines('unittest_objs_reference/')
    lines = lines[lines.index("ppp\n")+1:]
    lines = lines[lines.index("ppp\n")+1:]
    lines = [l.split() for l in lines]
    lines = list(itertools.chain.from_iterable(lines))
    lines = [float(i) for i in lines]
    return lines


class MyTestCase(unittest.TestCase):
    def test_vertices_equality(self):
        try:
            vertices_reference = get_vertices_reference()
        except IndexError as e:
            print("Error: ",e)

        try:
            vertices_received = get_vertices_received()
        except IndexError as e:
            print("Error: ",e)


        try:
            self.assertTrue(is_almost_equal(vertices_reference, vertices_received))
        except ListsLengthNotEqualError as e:
            print(e)


    def test_faces_equality(self):
        try:
            vertices_reference = get_faces_reference()
        except IndexError as e:
            print("Error: ",e)

        try:
            vertices_received = get_faces_received()
        except IndexError as e:
            print("Error: ",e)

        try:
            self.assertListEqual(vertices_reference, vertices_received, "Faces equal")
        except ListsLengthNotEqualError as e:
            print(e)

if __name__ == '__main__':
    unittest.main()
