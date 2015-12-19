from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length='255')
    email = models.CharField(max_length='1024')
    mobile_number = models.CharField(max_length='30')
    locale = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
        
    class Meta: 
        ordering = ['-created_at']