# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Common.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x43ommon.proto\x12\x06\x43ommon\"g\n\x07\x41\x64\x64ress\x12\r\n\x05Line1\x18\x01 \x01(\t\x12\r\n\x05Line2\x18\x02 \x01(\t\x12\r\n\x05Line3\x18\x03 \x01(\t\x12\x0c\n\x04\x43ity\x18\x04 \x01(\t\x12\r\n\x05State\x18\x05 \x01(\t\x12\x12\n\nPostalCode\x18\x06 \x01(\t\"2\n\tTelephone\x12\x10\n\x08\x41reaCode\x18\x01 \x01(\t\x12\x13\n\x0bPhoneNumber\x18\x02 \x01(\t\"\x81\x01\n\x0fPeriodCloseFile\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x1b\n\x13\x65nabledAtStoreClose\x18\x03 \x01(\x08\x12\x1b\n\x13\x65nabledAtShiftClose\x18\x04 \x01(\x08\x12\x1a\n\x12\x65nabledAtTillClose\x18\x05 \x01(\x08\"\xbb\x02\n\x10\x46tpConfiguration\x12\x16\n\x0eHostIdentifier\x18\x01 \x01(\x05\x12\x17\n\x0fHostDescription\x18\x02 \x01(\t\x12\x13\n\x0bHostAddress\x18\x03 \x01(\t\x12\x10\n\x08HostPort\x18\x04 \x01(\x05\x12\x10\n\x08UserName\x18\x05 \x01(\t\x12\x10\n\x08Password\x18\x06 \x01(\t\x12\x11\n\tFtpFolder\x18\x07 \x01(\t\x12\x14\n\x0cUseSecureFtp\x18\x08 \x01(\x08\x12\x0f\n\x07SendPjr\x18\t \x01(\x08\x12\x14\n\x0cSendWetstock\x18\n \x01(\x08\x12\x17\n\x0fUseImplicitFtps\x18\x0b \x01(\x08\x12\x12\n\nSendEopXml\x18\x0c \x01(\x08\x12\x19\n\x11SendFuelPriceData\x18\r \x01(\x08\x12\x13\n\x0bSendReports\x18\x0e \x01(\x08*E\n\x08Language\x12\x13\n\x0f\x44\x65\x66\x61ultLanguage\x10\x00\x12\x0b\n\x07\x45nglish\x10\x01\x12\n\n\x06\x46rench\x10\x02\x12\x0b\n\x07Spanish\x10\x03*(\n\x08\x43urrency\x12\x13\n\x0f\x44\x65\x66\x61ultCurrency\x10\x00\x12\x07\n\x03USD\x10\x01*@\n\nResultCode\x12\x0b\n\x07Success\x10\x00\x12\x15\n\x11ValidationFailure\x10\x01\x12\x0e\n\nFatalError\x10\x02*9\n\tFrequency\x12\x08\n\x04Once\x10\x00\x12\t\n\x05\x44\x61ily\x10\x01\x12\n\n\x06Weekly\x10\x02\x12\x0b\n\x07Monthly\x10\x03\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Common_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_LANGUAGE']._serialized_start=631
  _globals['_LANGUAGE']._serialized_end=700
  _globals['_CURRENCY']._serialized_start=702
  _globals['_CURRENCY']._serialized_end=742
  _globals['_RESULTCODE']._serialized_start=744
  _globals['_RESULTCODE']._serialized_end=808
  _globals['_FREQUENCY']._serialized_start=810
  _globals['_FREQUENCY']._serialized_end=867
  _globals['_ADDRESS']._serialized_start=24
  _globals['_ADDRESS']._serialized_end=127
  _globals['_TELEPHONE']._serialized_start=129
  _globals['_TELEPHONE']._serialized_end=179
  _globals['_PERIODCLOSEFILE']._serialized_start=182
  _globals['_PERIODCLOSEFILE']._serialized_end=311
  _globals['_FTPCONFIGURATION']._serialized_start=314
  _globals['_FTPCONFIGURATION']._serialized_end=629
# @@protoc_insertion_point(module_scope)