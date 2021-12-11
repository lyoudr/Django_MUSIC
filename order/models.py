from django.db import models
from django.contrib.auth.models import User

from product.models import ProductType, Product

import uuid

class PayInfo(models.Model):
    class Meta:
        db_table = 'PAY_INFO'
    
    CARD_TYPE_CHOICES = (
        ('1', 'VISA'),
        ('2', 'MASTER'),
        ('3', 'CREDIT')
    )
    BANK_CHOICES = (
        ('004', '台灣銀行'),
        ('005', '台灣土地銀行'),
        ('006', '合作金庫銀行'),
        ('007', '第一商業銀行'),
        ('008', '華南商業銀行'),
        ('009', '彰化商業銀行'),
        ('010', '花旗銀行')
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, related_name = 'pay_info')
    bank = models.CharField(max_length = 50, choices = BANK_CHOICES)
    card_no = models.CharField(max_length = 50)
    valid_no = models.CharField(max_length = 4)
    card_type = models.CharField(max_length = 1, choices = CARD_TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user.username}-{self.bank_name}'


class Order(models.Model): # 訂單
    class Meta:
        db_table = 'ORDER'
    
    STATUS_CHOICES = (
        ('01', '購物車'),
        ('02', '訂單'),
        ('03', '待出貨'),
        ('04', '已出貨'),
        ('05', '已送達')
    )

    order_no = models.CharField(max_length = 40) # 訂單編號
    status = models.CharField(max_length = 2, choices = STATUS_CHOICES) # 訂單狀態
    ship_addr = models.CharField(max_length = 100, null = True) # 送貨地址
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'order_b') # 買家
    pay_info = models.ForeignKey(PayInfo, on_delete=models.CASCADE, null = True) # 付款資訊
    product_type = models.ForeignKey(ProductType, on_delete = models.CASCADE) # 此訂單商品類別
    total_price = models.IntegerField(null = True) # 此訂單總價格
    created_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.order_no
    
    def save(self, *args, **kwargs):
        if self.order_no is None:
            unique_id = str(uuid.uuid4().hex.upper())
            self.order_no = f'{self.product_type.type_no}-{unique_id}-{self.order_user.pk}'
        super(Order, self).save(*args, **kwargs)

class OrderInfo(models.Model):
    class Meta:
        db_table = 'ORDER_INFO'
    
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'order_info_a')
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'order_info_b')
    count = models.IntegerField(default = 1)
    price = models.IntegerField() # 此筆 orderinfo 的總價 = product.price * count
    sell_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'order_a', default = 1) # 賣家
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'order_info_c', default = 1) # 放入購物車的人
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)

    def __str__(self):
        order_no = self.order.order_no if self.order else ''
        return f'{order_no}-{self.product.product_no}'
    
    def save(self, *args, **kwargs):
        if self.sell_user is None:
            self.sell_user = self.product.owner
        if self.price is None:
            self.price = self.product.price * self.count
        super(OrderInfo, self).save(*args, **kwargs)
    

    


 
    

