from django.db import models
from django.contrib.auth.models import User

from blog.models import BlogPost
from product.models import Product

class PayInfo(models.Model):
    class Meta:
        db_table = 'PAY_INFO'
    
    CARD_TYPE_CHOICES = (
        ('1', 'VISA'),
        ('2', 'MASTER'),
        ('3', 'CREDIT')
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, related_name = 'pay_info')
    bank_name = models.CharField(max_length = 50)
    bank_no = models.CharField(max_length = 50)
    card_no = models.CharField(max_length = 50)
    card_type = models.CharField(max_length = 1, choices = CARD_TYPE_CHOICES)

    def __str__(self):
        return f'{self.user.username}-{self.bank_name}'


class Order(models.Model):
    class Meta:
        db_table = 'ORDER'
    
    STATUS_CHOICES = (
        ('01', '購物車'),
        ('02', '訂單'),
        ('03', '待出貨'),
        ('04', '已出貨'),
        ('05', '已送達')
    )

    order_no = models.CharField(max_length = 40)
    status = models.CharField(max_length = 2, choices = STATUS_CHOICES)
    ship_addr = models.CharField(max_length = 100)
    sell_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'order_a') # 賣家
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'order_b') # 買家
    pay_info = models.ForeignKey(PayInfo, on_delete=models.CASCADE, null = True) # 付款資訊
    total_price = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.order_no


class OrderInfo(models.Model):
    class Meta:
        db_table = 'ORDER_INFO'
    
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'order_info_a')
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'order_info_b')
    count = models.IntegerField(default = 1)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.order.order_no}-{self.product.product_no}'
    

    


 
    

