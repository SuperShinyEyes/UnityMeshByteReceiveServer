#!/usr/bin/env python3
import os
import itertools
import types
def get_mesh_file_lines(dir_name):
    # dir_name = 'unittest_objs_reference/'
    all_file_names = os.listdir(dir_name)
    mesh_file_name = [i for i in all_file_names if i[-3:] == "obj"][0]
    mesh_file_path = os.path.join(dir_name, mesh_file_name)
    with open(mesh_file_path) as f:
        return f.readlines()

def get_vertices_received():
    lines = get_mesh_file_lines('unittest_objs_received/')
    lines = [l.split() for l in lines if l[0] == 'v']
    lines = list(itertools.chain.from_iterable(lines))
    lines = [float(i) for i in lines]
    return lines


def get_vertices_reference():
    lines = get_mesh_file_lines('unittest_objs_reference/')
    print(lines)
    lines = lines[:lines.index("ppp\n")]
    lines = [l.split() for l in lines]
    lines = list(itertools.chain.from_iterable(lines))
    lines = [float(i) for i in lines]
    return lines


if __name__ == '__main__':
    lines = get_vertices_reference()
    print(lines)
    print(type(lines[0]))
    print(isinstance(lines[0], float))