# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import notify_pb2 as notify__pb2


class NotifyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Notify = channel.unary_unary(
                '/notify.NotifyService/Notify',
                request_serializer=notify__pb2.NotifyRequest.SerializeToString,
                response_deserializer=notify__pb2.NotifyResponse.FromString,
                )


class NotifyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Notify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NotifyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Notify': grpc.unary_unary_rpc_method_handler(
                    servicer.Notify,
                    request_deserializer=notify__pb2.NotifyRequest.FromString,
                    response_serializer=notify__pb2.NotifyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'notify.NotifyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NotifyService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Notify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/notify.NotifyService/Notify',
            notify__pb2.NotifyRequest.SerializeToString,
            notify__pb2.NotifyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
