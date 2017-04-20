#!/usr/bin/env python3


class Vector3(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Mesh(object):

    def __init__(self, vertices, triangle_indicies):
        self.vertices = vertices
        self.triangles = triangle_indicies