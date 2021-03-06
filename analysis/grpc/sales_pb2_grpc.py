# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import sales_pb2 as sales__pb2


class SalesReportStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListProduct = channel.unary_stream(
                '/sales.SalesReport/ListProduct',
                request_serializer=sales__pb2.ProductRe.SerializeToString,
                response_deserializer=sales__pb2.Product.FromString,
                )
        self.CreateFeedBack = channel.unary_unary(
                '/sales.SalesReport/CreateFeedBack',
                request_serializer=sales__pb2.FeedBack.SerializeToString,
                response_deserializer=sales__pb2.FeedBack.FromString,
                )
        self.CreateKeyWord = channel.unary_unary(
                '/sales.SalesReport/CreateKeyWord',
                request_serializer=sales__pb2.KeyWord.SerializeToString,
                response_deserializer=sales__pb2.KeyWord.FromString,
                )


class SalesReportServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateFeedBack(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateKeyWord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SalesReportServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListProduct': grpc.unary_stream_rpc_method_handler(
                    servicer.ListProduct,
                    request_deserializer=sales__pb2.ProductRe.FromString,
                    response_serializer=sales__pb2.Product.SerializeToString,
            ),
            'CreateFeedBack': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateFeedBack,
                    request_deserializer=sales__pb2.FeedBack.FromString,
                    response_serializer=sales__pb2.FeedBack.SerializeToString,
            ),
            'CreateKeyWord': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateKeyWord,
                    request_deserializer=sales__pb2.KeyWord.FromString,
                    response_serializer=sales__pb2.KeyWord.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sales.SalesReport', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SalesReport(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/sales.SalesReport/ListProduct',
            sales__pb2.ProductRe.SerializeToString,
            sales__pb2.Product.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateFeedBack(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sales.SalesReport/CreateFeedBack',
            sales__pb2.FeedBack.SerializeToString,
            sales__pb2.FeedBack.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateKeyWord(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sales.SalesReport/CreateKeyWord',
            sales__pb2.KeyWord.SerializeToString,
            sales__pb2.KeyWord.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
