from django.db import models
# Create your models here.
#main sale model where the user can set the price of the book they are gonna
#sell
class Sale(models.Model):
    seller_id = models.CharField(max_length=500)
    seller_username = models.CharField(max_length=500)
    book = models.ForeignKey('search.Book')
    description = models.TextField()
    price = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.seller_username)
        
    class Meta:
        ordering = ['-created_at']
        
        
#the below model is for user's who are interested in a sale        
class SaleInterest(models.Model):
    interested_user_id = models.CharField(max_length=500)
    interested_username = models.CharField(max_length=500)
    sale_id = models.ForeignKey('Sale')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return '{}'.format(self.interested_username)
        
    class Meta:
        ordering = ['-created_at']
    