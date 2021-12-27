from analysis.grpc import sales_pb2_grpc, sales_pb2

import grpc
import os

class GrpcClient:
    def __init__(self):
        channel = grpc.insecure_channel(os.getenv("GRPC_HOST"))
        self.stub = sales_pb2_grpc.SalesReportStub(channel)
    
    def get_analysis(self):
        sales = self.stub.ListProduct(sales_pb2.ProductRe())
        resp = [{
            'product_name': sale.product_name,
            'product_type': sale.product_type,
            'product_no': sale.product_no,
            'rank': sale.rank
        } for sale in sales]
        return resp

    def post_feedback(self, data, user_id):
        feedback = self.stub.CreateFeedBack(sales_pb2.FeedBack(
            rank = data.get('rank'),
            user_id = user_id,
            product_type_id = data.get('product_type_id'),
            description = data.get('description')
        ))
        return feedback

    def post_keyword(self, data, user_id):
        keyword = self.stub.CreateKeyWord(sales_pb2.KeyWord(
            user_id = user_id,
            keyword = data.get('keyword')
        ))
        return keyword
