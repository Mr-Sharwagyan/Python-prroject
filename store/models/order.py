from django.db import models

STATUS_CHOICE = (
    ('Pending', 'Pending'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
)

class OrderDetail(models.Model):
    user= models.BigIntegerField(default=True)
    product_name=models.CharField(max_length=250)
    image = models.ImageField(null=True,blank=True)
    quantity=models.PositiveIntegerField(default=1)
    price=models.BigIntegerField()
    ordered_date = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,default='Pending',choices=STATUS_CHOICE)
