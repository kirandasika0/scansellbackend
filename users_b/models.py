from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(default='', max_length='255')
    username = models.CharField(max_length='255')
    password = models.CharField(default='', max_length='1024')
    email = models.CharField(max_length='1024')
    mobile_number = models.CharField(max_length='30')
    locale = models.TextField()
    redis_key = models.CharField(default='', max_length='255')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
        
    class Meta: 
        ordering = ['-created_at']