import numpy

class Foo:

    def __init__(self):
        self.vertices = None
        self.faces = None
        self.normals_reference = None
        self.normals_test = None


    def normalize_v3(self, arr):
        ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
        lens = numpy.sqrt(arr[:, 0] ** 2 + arr[:, 1] ** 2 + arr[:, 2] ** 2)
        arr[:, 0] /= lens
        arr[:, 1] /= lens
        arr[:, 2] /= lens
        return arr

    def compare_normals(self):
        vertices = self.vertices
        faces = self.faces
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

        numpy.savetxt('normals_test.obj', norm, delimiter=',')

        return norm == self.normals_reference

    def run(self):

        with open('vertices.obj') as f:
            lines = f.readlines()
            self.vertices = numpy.array([
                    [
                    # float(line[2,:].split()[0]),
                    # float(line[2,:].split()[1]),
                    # float(line[2,:].split()[2])
                    float(line.split()[1:][0]),
                        float(line.split()[1:][1]),
                        float(line.split()[1:][2])

                    ] for line in lines if line[0] == "v"

            ])
            print(len(self.vertices), self.vertices)

        with open('faces.obj') as f:
            lines = f.readlines()
            self.faces = numpy.array([
                    [
                        int(line.split()[1:][0].split('//')[0]),
                        int(line.split()[1:][1].split('//')[0]),
                        int(line.split()[1:][2].split('//')[0])

                    ] for line in lines if line[0] == "f"

            ])
            # self.faces -= 1
            # print(self.faces)

        with open('normals.obj') as f:
            lines = f.readlines()
            self.normals_reference = numpy.array([
                    [
                    # float(line[2,:].split()[0]),
                    # float(line[2,:].split()[1]),
                    # float(line[2,:].split()[2])
                    float(line.split()[1:][0]),
                        float(line.split()[1:][1]),
                        float(line.split()[1:][2])

                    ] for line in lines if line[0:2] == "vn"

            ])
            print(self.normals_reference)

        print(self.compare_normals())



if __name__ == '__main__':
    foo = Foo()
    foo.run()