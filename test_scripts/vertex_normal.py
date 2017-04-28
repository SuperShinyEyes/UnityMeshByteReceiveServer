# https://sites.google.com/site/dlampetest/python/calculating-normals-of-a-triangle-mesh-using-numpy

import numpy

vertices = numpy.array([[ 0.82667452,  0.89591247,  0.91638623],
                        [ 0.10045271,  0.50575086,  0.73920507],
                        [ 0.06341482,  0.17413744,  0.6316301 ],
                        [ 0.75613029,  0.82585983,  0.10012549],
                        [ 0.45498342,  0.5636221 ,  0.10940527],
                        [ 0.46079863,  0.54088544,  0.1519899 ],
                        [ 0.61961934,  0.78550213,  0.43406491],
                        [ 0.12654252,  0.7514213 ,  0.18265301],
                        [ 0.94441365,  0.00428673,  0.46893573],
                        [ 0.79083297,  0.70198129,  0.75670947]] )
faces = numpy.array( [ [0,1,2],
                       [0,2,3],
                       [1,2,3],
                       [1,4,5],
                       [2,5,6],
                       [6,3,7],
                       [9,8,7] ] )


def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    lens = numpy.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    arr[:,0] /= lens
    arr[:,1] /= lens
    arr[:,2] /= lens
    return arr


#Create a zeroed array with the same type and shape as our vertices i.e., per vertex normal
norm = numpy.zeros( vertices.shape, dtype=vertices.dtype )
#Create an indexed view into the vertex array using the array of three indices for triangles
tris = vertices[faces]
#Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle
n = numpy.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )
# n is now an array of normals per triangle. The length of each normal is dependent the vertices,
# we need to normalize these, so that our next step weights each normal equally.
normalize_v3(n)
# now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
# But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle,
# the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to normalize again afterwards.
# The cool part, we can actually add the normals through an indexed view of our (zeroed) per vertex normal array
norm[ faces[:,0] ] += n
norm[ faces[:,1] ] += n
norm[ faces[:,2] ] += n
normalize_v3(norm)

print(norm)

numpy.array( [
    i for i in range(10)

])