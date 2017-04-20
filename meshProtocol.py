from protobuf3.message import Message
from protobuf3.fields import UInt32Field, EnumField, UInt64Field, MessageField, FloatField
from enum import Enum


class Vec3D(Message):
    pass


class Vec4D(Message):
    pass


class Face(Message):
    pass


class Mesh(Message):
    pass


class LocationRequest(Message):
    pass


class LocationResponse(Message):
    pass


class Message(Message):

    class Type(Enum):
        MESH = 0
        LOCATION_REQUEST = 1
        LOCATION_RESPONSE = 2

Vec3D.add_field('x', FloatField(field_number=1, optional=True))
Vec3D.add_field('y', FloatField(field_number=2, optional=True))
Vec3D.add_field('z', FloatField(field_number=3, optional=True))
Vec4D.add_field('x', FloatField(field_number=1, optional=True))
Vec4D.add_field('y', FloatField(field_number=2, optional=True))
Vec4D.add_field('z', FloatField(field_number=3, optional=True))
Vec4D.add_field('w', FloatField(field_number=4, optional=True))
Face.add_field('v1', UInt32Field(field_number=1, optional=True))
Face.add_field('v2', UInt32Field(field_number=2, optional=True))
Face.add_field('v3', UInt32Field(field_number=3, optional=True))
Mesh.add_field('mesh_id', UInt32Field(field_number=2, optional=True))
Mesh.add_field('timestamp', UInt64Field(field_number=3, optional=True))
Mesh.add_field('cam_position', MessageField(field_number=100, optional=True, message_cls=Vec3D))
Mesh.add_field('cam_rotation', MessageField(field_number=101, optional=True, message_cls=Vec4D))
Mesh.add_field('vertices', MessageField(field_number=200, repeated=True, message_cls=Vec3D))
Mesh.add_field('faces', MessageField(field_number=201, repeated=True, message_cls=Face))
LocationResponse.add_field('location', MessageField(field_number=1, optional=True, message_cls=Vec3D))
LocationResponse.add_field('orientation', MessageField(field_number=2, optional=True, message_cls=Vec3D))
Message.add_field('type', EnumField(field_number=1, optional=True, enum_cls=Message.Type))
Message.add_field('device_id', UInt32Field(field_number=2, optional=True))
Message.add_field('mesh', MessageField(field_number=100, optional=True, message_cls=Mesh))
Message.add_field('location_request', MessageField(field_number=300, optional=True, message_cls=LocationRequest))
Message.add_field('location_response', MessageField(field_number=400, optional=True, message_cls=LocationResponse))
