# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protos_pb2 as protos__pb2


class ArticleServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetMessages = channel.unary_stream(
                '/chat.ArticleService/GetMessages',
                request_serializer=protos__pb2.MessageRequest.SerializeToString,
                response_deserializer=protos__pb2.Message.FromString,
                )
        self.SendMessage = channel.unary_unary(
                '/chat.ArticleService/SendMessage',
                request_serializer=protos__pb2.SendRequest.SerializeToString,
                response_deserializer=protos__pb2.Status.FromString,
                )
        self.GetGroups = channel.unary_stream(
                '/chat.ArticleService/GetGroups',
                request_serializer=protos__pb2.Server.SerializeToString,
                response_deserializer=protos__pb2.Group.FromString,
                )
        self.RegisterGroup = channel.unary_unary(
                '/chat.ArticleService/RegisterGroup',
                request_serializer=protos__pb2.Group.SerializeToString,
                response_deserializer=protos__pb2.Status.FromString,
                )
        self.ConnectToGroup = channel.unary_unary(
                '/chat.ArticleService/ConnectToGroup',
                request_serializer=protos__pb2.Client.SerializeToString,
                response_deserializer=protos__pb2.Status.FromString,
                )
        self.DisconnectFromGroup = channel.unary_unary(
                '/chat.ArticleService/DisconnectFromGroup',
                request_serializer=protos__pb2.Client.SerializeToString,
                response_deserializer=protos__pb2.Status.FromString,
                )


class ArticleServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGroups(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectToGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisconnectFromGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ArticleServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMessages,
                    request_deserializer=protos__pb2.MessageRequest.FromString,
                    response_serializer=protos__pb2.Message.SerializeToString,
            ),
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=protos__pb2.SendRequest.FromString,
                    response_serializer=protos__pb2.Status.SerializeToString,
            ),
            'GetGroups': grpc.unary_stream_rpc_method_handler(
                    servicer.GetGroups,
                    request_deserializer=protos__pb2.Server.FromString,
                    response_serializer=protos__pb2.Group.SerializeToString,
            ),
            'RegisterGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterGroup,
                    request_deserializer=protos__pb2.Group.FromString,
                    response_serializer=protos__pb2.Status.SerializeToString,
            ),
            'ConnectToGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.ConnectToGroup,
                    request_deserializer=protos__pb2.Client.FromString,
                    response_serializer=protos__pb2.Status.SerializeToString,
            ),
            'DisconnectFromGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.DisconnectFromGroup,
                    request_deserializer=protos__pb2.Client.FromString,
                    response_serializer=protos__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chat.ArticleService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ArticleService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chat.ArticleService/GetMessages',
            protos__pb2.MessageRequest.SerializeToString,
            protos__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ArticleService/SendMessage',
            protos__pb2.SendRequest.SerializeToString,
            protos__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGroups(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chat.ArticleService/GetGroups',
            protos__pb2.Server.SerializeToString,
            protos__pb2.Group.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RegisterGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ArticleService/RegisterGroup',
            protos__pb2.Group.SerializeToString,
            protos__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectToGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ArticleService/ConnectToGroup',
            protos__pb2.Client.SerializeToString,
            protos__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DisconnectFromGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ArticleService/DisconnectFromGroup',
            protos__pb2.Client.SerializeToString,
            protos__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)