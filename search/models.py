from django.db import models
# Create your models here.
class Book(models.Model):
    full_title = models.TextField()
    link = models.TextField()
    uniform_title = models.TextField()
    #it's the same as the isbn number - metadata purpose
    ean_13 = models.CharField(max_length=300, default='') 
    
    def __str__(self):
        return self.uniform_title
        
    
class Product(models.Model):
    full_title = models.TextField()
    link = models.TextField()
    uniform_title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.uniform_title