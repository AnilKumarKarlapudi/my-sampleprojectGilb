# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: CrindMerchandising.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import libs.grpc.resources.compiled_protos.Common_pb2 as Common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x18\x43rindMerchandising.proto\x1a\x0c\x43ommon.proto"\x1c\n\x1aGetCrindMerchandiseRequest"K\n\x18GetCrindMerchandiseReply\x12/\n\x12\x43rindMerchandising\x18\x01 \x01(\x0b\x32\x13.CrindMerchandising"M\n\x1aSetCrindMerchandiseRequest\x12/\n\x12\x43rindMerchandising\x18\x01 \x01(\x0b\x32\x13.CrindMerchandising"A\n\x18SetCrindMerchandiseReply\x12\x0f\n\x07Success\x18\x01 \x01(\x08\x12\x14\n\x0c\x45rrorMessage\x18\x02 \x01(\t"Z\n#SetCrindMerchandisingEnabledRequest\x12\x0f\n\x07\x45nabled\x18\x01 \x01(\x08\x12"\n\x08Language\x18\x02 \x01(\x0e\x32\x10.Common.Language"J\n!SetCrindMerchandisingEnabledReply\x12\x0f\n\x07Success\x18\x01 \x01(\x08\x12\x14\n\x0c\x45rrorMessage\x18\x02 \x01(\t"u\n\x12\x43rindMerchandising\x12\x0f\n\x07\x45nabled\x18\x01 \x01(\x08\x12\x12\n\nVendorName\x18\x02 \x01(\t\x12\x16\n\x0ePromptLocation\x18\x03 \x01(\x05\x12"\n\nCategories\x18\x04 \x03(\x0b\x32\x0e.MerchCategory"N\n\rMerchCategory\x12\x0c\n\x04Name\x18\x01 \x01(\t\x12\x19\n\x05Items\x18\x02 \x03(\x0b\x32\n.MerchItem\x12\x14\n\x0c\x44isplayOrder\x18\x03 \x01(\x05"V\n\tMerchItem\x12\x0b\n\x03Plu\x18\x01 \x01(\t\x12\x13\n\x0b\x44\x65scription\x18\x02 \x01(\t\x12\x11\n\tAvailable\x18\x03 \x01(\x08\x12\x14\n\x0c\x44isplayOrder\x18\x04 \x01(\x05\x32\xa3\x02\n\x19\x43rindMerchandisingService\x12M\n\x13GetCrindMerchandise\x12\x1b.GetCrindMerchandiseRequest\x1a\x19.GetCrindMerchandiseReply\x12M\n\x13SetCrindMerchandise\x12\x1b.SetCrindMerchandiseRequest\x1a\x19.SetCrindMerchandiseReply\x12h\n\x1cSetCrindMerchandisingEnabled\x12$.SetCrindMerchandisingEnabledRequest\x1a".SetCrindMerchandisingEnabledReplyB!\xaa\x02\x1eGilbarco.POS.FuelConfigurationb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "CrindMerchandising_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\252\002\036Gilbarco.POS.FuelConfiguration"
    _globals["_GETCRINDMERCHANDISEREQUEST"]._serialized_start = 42
    _globals["_GETCRINDMERCHANDISEREQUEST"]._serialized_end = 70
    _globals["_GETCRINDMERCHANDISEREPLY"]._serialized_start = 72
    _globals["_GETCRINDMERCHANDISEREPLY"]._serialized_end = 147
    _globals["_SETCRINDMERCHANDISEREQUEST"]._serialized_start = 149
    _globals["_SETCRINDMERCHANDISEREQUEST"]._serialized_end = 226
    _globals["_SETCRINDMERCHANDISEREPLY"]._serialized_start = 228
    _globals["_SETCRINDMERCHANDISEREPLY"]._serialized_end = 293
    _globals["_SETCRINDMERCHANDISINGENABLEDREQUEST"]._serialized_start = 295
    _globals["_SETCRINDMERCHANDISINGENABLEDREQUEST"]._serialized_end = 385
    _globals["_SETCRINDMERCHANDISINGENABLEDREPLY"]._serialized_start = 387
    _globals["_SETCRINDMERCHANDISINGENABLEDREPLY"]._serialized_end = 461
    _globals["_CRINDMERCHANDISING"]._serialized_start = 463
    _globals["_CRINDMERCHANDISING"]._serialized_end = 580
    _globals["_MERCHCATEGORY"]._serialized_start = 582
    _globals["_MERCHCATEGORY"]._serialized_end = 660
    _globals["_MERCHITEM"]._serialized_start = 662
    _globals["_MERCHITEM"]._serialized_end = 748
    _globals["_CRINDMERCHANDISINGSERVICE"]._serialized_start = 751
    _globals["_CRINDMERCHANDISINGSERVICE"]._serialized_end = 1042
# @@protoc_insertion_point(module_scope)
