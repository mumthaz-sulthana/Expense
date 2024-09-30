from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    
    name=models.CharField(max_length=200)
    
    budget=models.PositiveIntegerField()
    
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        
        unique_together=("name","owner")
    
    def __str__(self):
        return self.name
    
class Transactions(models.Model):
    
    title=models.CharField(max_length=200)
    
    amount=models.PositiveIntegerField()
    
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    payment_options={
        ("cash","cash"),
        ("upi","upi"),
        ("card","card")
    }
    
    payment_method=models.CharField(max_length=200,choices=payment_options,default="cash")
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    