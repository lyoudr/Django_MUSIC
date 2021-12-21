from analysis.grpc import sales_pb2_grpc, sales_pb2

import grpc
import os

def get_analysis():
    print('grpc_host is =>', f'{os.getenv("GRPC_HOST")}:5100')
    with grpc.insecure_channel(f'{os.getenv("GRPC_HOST")}:5100') as channel:
        stub = sales_pb2_grpc.SalesReportStub(channel)
        sales = stub.ListProduct(sales_pb2.ProductRe())
        resp = [{
                'product_name': sale.product_name,
                'product_type': sale.product_type,
                'product_no': sale.product_no,
                'rank': sale.rank
            } for sale in sales]
        return resp