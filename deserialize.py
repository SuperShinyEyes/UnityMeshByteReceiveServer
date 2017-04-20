#!/usr/bin/env python3

from struct import unpack
import UnityMeshObjectModel
'''
/// <summary>
/// Deserializes a list of Mesh objects from the provided byte array.
/// </summary>
/// <param name="data">Binary data to be deserialized into a list of Mesh objects.</param>
/// <returns>List of Mesh objects.</returns>
public static IEnumerable<Mesh> Deserialize(byte[] data)
{
    List<Mesh> meshes = new List<Mesh>();

    using (MemoryStream stream = new MemoryStream(data))
    {
        using (BinaryReader reader = new BinaryReader(stream))
        {
            while (reader.BaseStream.Length - reader.BaseStream.Position >= HeaderSize)
            {
                meshes.Add(ReadMesh(reader));
            }
        }
    }

    return meshes;
}

/// <summary>
/// Reads a single Mesh object from the data stream.
/// </summary>
/// <param name="reader">BinaryReader representing the data stream.</param>
/// <returns>Mesh object read from the stream.</returns>
private static Mesh ReadMesh(BinaryReader reader)
  {
      SysDiag.Debug.Assert(reader != null);

      int vertexCount = 0;
       int triangleIndexCount = 0;

       // Read the mesh data.
       ReadMeshHeader(reader, out vertexCount, out triangleIndexCount);
       Vector3[] vertices = ReadVertices(reader, vertexCount);
       int[] triangleIndices = ReadTriangleIndicies(reader, triangleIndexCount);

       // Create the mesh.
       Mesh mesh = new Mesh();
       mesh.vertices = vertices;
       mesh.triangles = triangleIndices;
       // Reconstruct the normals from the vertices and triangles.
       mesh.RecalculateNormals();

       return mesh;
  }

/// <summary>
/// Reads a mesh header from the data stream.
/// </summary>
/// <param name="reader">BinaryReader representing the data stream.</param>
/// <param name="vertexCount">Count of vertices in the mesh.</param>
/// <param name="triangleIndexCount">Count of triangle indices in the mesh.</param>
private static void ReadMeshHeader(BinaryReader reader, out int vertexCount, out int triangleIndexCount)
  {
      SysDiag.Debug.Assert(reader != null);

      vertexCount = reader.ReadInt32();
      triangleIndexCount = reader.ReadInt32();
  }


  /// <summary>
  /// Reads a mesh's vertices from the data stream.
  /// </summary>
  /// <param name="reader">BinaryReader representing the data stream.</param>
  /// <param name="vertexCount">Count of vertices to read.</param>
  /// <returns>Array of Vector3 structures representing the mesh's vertices.</returns>
  private static Vector3[] ReadVertices(BinaryReader reader, int vertexCount)
  {
      SysDiag.Debug.Assert(reader != null);

      Vector3[] vertices = new Vector3[vertexCount];

      for (int i = 0; i < vertices.Length; i++)
      {
          vertices[i] = new Vector3(reader.ReadSingle(),
                                  reader.ReadSingle(),
                                  reader.ReadSingle());
      }

      return vertices;
  }

/// <summary>
/// Reads the vertex indices that represent a mesh's triangles from the data stream
/// </summary>
/// <param name="reader">BinaryReader representing the data stream.</param>
/// <param name="triangleIndexCount">Count of indices to read.</param>
/// <returns>Array of integers that describe how the vertex indices form triangles.</returns>
private static int[] ReadTriangleIndicies(BinaryReader reader, int triangleIndexCount)
{
  SysDiag.Debug.Assert(reader != null);

  int[] triangleIndices = new int[triangleIndexCount];

  for (int i = 0; i < triangleIndices.Length; i++)
  {
      triangleIndices[i] = reader.ReadInt32();
  }

  return triangleIndices;
}
'''

class EmptyByteError(Exception):
    pass

def is_empty_byte(data):
    return len(data) == 0

def deserialize(stream):
    '''
    :param stream: byte 
    :return: 
    '''

    meshes = []
    # Two c# Int32: 4 * 2 = 8
    header_size = 8
    reader_pos = 0
    stream_len = len(stream)
    while stream_len - reader_pos >= header_size:
        meshes.append(read_mesh(stream))

def write_meshes(meshes):
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
        i = 1
        for mesh in meshes:
            write_mesh(f, mesh)


def write_mesh(stream: _io.TextIOWrapper, mesh: UnityMeshObjectModel.Mesh, index):
        header = 'o Object.{}'.format(index)
        stream.write(header)

        # for v in mesh.vertices:
        #     line = "v {x} {y} {z}".format(x=v.x, y=v.y, z=v.z)

        lines = ["v {x} {y} {z}".format(x=v.x, y=v.y, z=v.z) for v in mesh.vertices]
        stream.writelines(lines)
        stream.write("\n\n")




def read_mesh(stream):

    vertex_count, triangle_index_count = read_mesh_header(stream)
    vertices = read_vertices(stream, vertex_count)
    triangle_indicies = read_triangle_indicies(stream, triangle_index_count)
    mesh = UnityMeshObjectModel.Mesh(vertices, triangle_indicies)
    return mesh


    

def read_mesh_header(stream) -> object:
    '''
    :param stream: 
    :return: 
    '''
    vertex_count = read_int32(stream)
    triangleIndexCount = read_int32(stream)
    return vertex_count, triangleIndexCount

def read_vertices(stream, vertexCount):
    '''
    Vector3[] vertices = new Vector3[vertexCount];
    :param vertexCount: 
    :param stream: 
    :return: 
    '''
    vertices = [
        UnityMeshObjectModel.Vector3(
            read_int32(stream),
            read_int32(stream),
            read_int32(stream)
        ) for _ in range(vertexCount)
    ]
    return vertices

def read_triangle_indicies(stream, triangleIndexCount):
    '''
    Vector3[] vertices = new Vector3[vertexCount];
    :param triangleIndexCount: 
    :param stream: 
    :return: 
    '''
    triangleIndicies = [
        read_int32(stream) for _ in range(vertexCount)
    ]
    return triangleIndicies






def read_int32(stream):
    '''
    Read 4 byte from data
    :param stream: 
    :return: truncated data and int
    '''
    # if is_empty_byte(data):
    #     raise EmptyByteError

    int32, = unpack('i', stream.read(4))
    return int32