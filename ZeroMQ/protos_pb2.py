# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cprotos.proto\x12\x04\x63hat\x1a\x1fgoogle/protobuf/timestamp.proto\"\x83\x01\n\x07Message\x12\x13\n\x06\x61uthor\x18\x01 \x01(\tH\x00\x88\x01\x01\x12-\n\x04time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x01\x88\x01\x01\x12\x14\n\x07\x63ontent\x18\x03 \x01(\tH\x02\x88\x01\x01\x42\t\n\x07_authorB\x07\n\x05_timeB\n\n\x08_content\"h\n\x0eMessageRequest\x12\x13\n\x06\x61uthor\x18\x01 \x01(\tH\x00\x88\x01\x01\x12-\n\x04time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x01\x88\x01\x01\x42\t\n\x07_authorB\x07\n\x05_time\"$\n\x06\x43lient\x12\x11\n\x04uuid\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x07\n\x05_uuid\"l\n\x0bSendRequest\x12!\n\x06\x63lient\x18\x01 \x01(\x0b\x32\x0c.chat.ClientH\x00\x88\x01\x01\x12#\n\x07message\x18\x02 \x01(\x0b\x32\r.chat.MessageH\x01\x88\x01\x01\x42\t\n\x07_clientB\n\n\x08_message\"[\n\x06Status\x12(\n\x06status\x18\x01 \x01(\x0e\x32\x13.chat.Status.StatusH\x00\x88\x01\x01\"\x1c\n\x06Status\x12\x06\n\x02ok\x10\x00\x12\n\n\x06\x64\x65nied\x10\x01\x42\t\n\x07_status\"=\n\x07\x41\x64\x64ress\x12\x0f\n\x02ip\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x11\n\x04port\x18\x02 \x01(\x05H\x01\x88\x01\x01\x42\x05\n\x03_ipB\x07\n\x05_port\"T\n\x05Group\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12#\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\r.chat.AddressH\x01\x88\x01\x01\x42\x07\n\x05_nameB\n\n\x08_address\"\x08\n\x06Server2\xb9\x02\n\x0e\x41rticleService\x12\x36\n\x0bGetMessages\x12\x14.chat.MessageRequest\x1a\r.chat.Message\"\x00\x30\x01\x12\x30\n\x0bSendMessage\x12\x11.chat.SendRequest\x1a\x0c.chat.Status\"\x00\x12*\n\tGetGroups\x12\x0c.chat.Server\x1a\x0b.chat.Group\"\x00\x30\x01\x12,\n\rRegisterGroup\x12\x0b.chat.Group\x1a\x0c.chat.Status\"\x00\x12.\n\x0e\x43onnectToGroup\x12\x0c.chat.Client\x1a\x0c.chat.Status\"\x00\x12\x33\n\x13\x44isconnectFromGroup\x12\x0c.chat.Client\x1a\x0c.chat.Status\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MESSAGE']._serialized_start=56
  _globals['_MESSAGE']._serialized_end=187
  _globals['_MESSAGEREQUEST']._serialized_start=189
  _globals['_MESSAGEREQUEST']._serialized_end=293
  _globals['_CLIENT']._serialized_start=295
  _globals['_CLIENT']._serialized_end=331
  _globals['_SENDREQUEST']._serialized_start=333
  _globals['_SENDREQUEST']._serialized_end=441
  _globals['_STATUS']._serialized_start=443
  _globals['_STATUS']._serialized_end=534
  _globals['_STATUS_STATUS']._serialized_start=495
  _globals['_STATUS_STATUS']._serialized_end=523
  _globals['_ADDRESS']._serialized_start=536
  _globals['_ADDRESS']._serialized_end=597
  _globals['_GROUP']._serialized_start=599
  _globals['_GROUP']._serialized_end=683
  _globals['_SERVER']._serialized_start=685
  _globals['_SERVER']._serialized_end=693
  _globals['_ARTICLESERVICE']._serialized_start=696
  _globals['_ARTICLESERVICE']._serialized_end=1009
# @@protoc_insertion_point(module_scope)