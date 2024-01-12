# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import libs.grpc.resources.compiled_protos.FeatureActivation_pb2 as FeatureActivation__pb2


class FeatureActivationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ActivateFeatures = channel.unary_unary(
            "/FeatureActivationService/ActivateFeatures",
            request_serializer=FeatureActivation__pb2.ActivateFeaturesRequest.SerializeToString,
            response_deserializer=FeatureActivation__pb2.ActivateFeaturesReply.FromString,
        )
        self.GetFeatureConfiguration = channel.unary_unary(
            "/FeatureActivationService/GetFeatureConfiguration",
            request_serializer=FeatureActivation__pb2.GetFeatureConfigurationRequest.SerializeToString,
            response_deserializer=FeatureActivation__pb2.GetFeatureConfigurationReply.FromString,
        )
        self.GetBundles = channel.unary_unary(
            "/FeatureActivationService/GetBundles",
            request_serializer=FeatureActivation__pb2.GetBundlesRequest.SerializeToString,
            response_deserializer=FeatureActivation__pb2.GetBundlesReply.FromString,
        )
        self.UpdateBundle = channel.unary_unary(
            "/FeatureActivationService/UpdateBundle",
            request_serializer=FeatureActivation__pb2.UpdateBundleRequest.SerializeToString,
            response_deserializer=FeatureActivation__pb2.UpdateBundleReply.FromString,
        )
        self.GetUpgradeApprovalStatus = channel.unary_unary(
            "/FeatureActivationService/GetUpgradeApprovalStatus",
            request_serializer=FeatureActivation__pb2.GetUpgradeApprovalStatusRequest.SerializeToString,
            response_deserializer=FeatureActivation__pb2.GetUpgradeApprovalStatusReply.FromString,
        )
        self.SetUpgradeApprovalStatus = channel.unary_unary(
            "/FeatureActivationService/SetUpgradeApprovalStatus",
            request_serializer=FeatureActivation__pb2.SetUpgradeApprovalStatusRequest.SerializeToString,
            response_deserializer=FeatureActivation__pb2.SetUpgradeApprovalStatusReply.FromString,
        )


class FeatureActivationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ActivateFeatures(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetFeatureConfiguration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetBundles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateBundle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetUpgradeApprovalStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SetUpgradeApprovalStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_FeatureActivationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ActivateFeatures": grpc.unary_unary_rpc_method_handler(
            servicer.ActivateFeatures,
            request_deserializer=FeatureActivation__pb2.ActivateFeaturesRequest.FromString,
            response_serializer=FeatureActivation__pb2.ActivateFeaturesReply.SerializeToString,
        ),
        "GetFeatureConfiguration": grpc.unary_unary_rpc_method_handler(
            servicer.GetFeatureConfiguration,
            request_deserializer=FeatureActivation__pb2.GetFeatureConfigurationRequest.FromString,
            response_serializer=FeatureActivation__pb2.GetFeatureConfigurationReply.SerializeToString,
        ),
        "GetBundles": grpc.unary_unary_rpc_method_handler(
            servicer.GetBundles,
            request_deserializer=FeatureActivation__pb2.GetBundlesRequest.FromString,
            response_serializer=FeatureActivation__pb2.GetBundlesReply.SerializeToString,
        ),
        "UpdateBundle": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateBundle,
            request_deserializer=FeatureActivation__pb2.UpdateBundleRequest.FromString,
            response_serializer=FeatureActivation__pb2.UpdateBundleReply.SerializeToString,
        ),
        "GetUpgradeApprovalStatus": grpc.unary_unary_rpc_method_handler(
            servicer.GetUpgradeApprovalStatus,
            request_deserializer=FeatureActivation__pb2.GetUpgradeApprovalStatusRequest.FromString,
            response_serializer=FeatureActivation__pb2.GetUpgradeApprovalStatusReply.SerializeToString,
        ),
        "SetUpgradeApprovalStatus": grpc.unary_unary_rpc_method_handler(
            servicer.SetUpgradeApprovalStatus,
            request_deserializer=FeatureActivation__pb2.SetUpgradeApprovalStatusRequest.FromString,
            response_serializer=FeatureActivation__pb2.SetUpgradeApprovalStatusReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("FeatureActivationService", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class FeatureActivationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ActivateFeatures(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FeatureActivationService/ActivateFeatures",
            FeatureActivation__pb2.ActivateFeaturesRequest.SerializeToString,
            FeatureActivation__pb2.ActivateFeaturesReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetFeatureConfiguration(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FeatureActivationService/GetFeatureConfiguration",
            FeatureActivation__pb2.GetFeatureConfigurationRequest.SerializeToString,
            FeatureActivation__pb2.GetFeatureConfigurationReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetBundles(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FeatureActivationService/GetBundles",
            FeatureActivation__pb2.GetBundlesRequest.SerializeToString,
            FeatureActivation__pb2.GetBundlesReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpdateBundle(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FeatureActivationService/UpdateBundle",
            FeatureActivation__pb2.UpdateBundleRequest.SerializeToString,
            FeatureActivation__pb2.UpdateBundleReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetUpgradeApprovalStatus(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FeatureActivationService/GetUpgradeApprovalStatus",
            FeatureActivation__pb2.GetUpgradeApprovalStatusRequest.SerializeToString,
            FeatureActivation__pb2.GetUpgradeApprovalStatusReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def SetUpgradeApprovalStatus(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FeatureActivationService/SetUpgradeApprovalStatus",
            FeatureActivation__pb2.SetUpgradeApprovalStatusRequest.SerializeToString,
            FeatureActivation__pb2.SetUpgradeApprovalStatusReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )