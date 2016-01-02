import redis
from users_b.models import User
#Creating new redis server
r = redis.Redis(host='pub-redis-18592.us-east-1-2.4.ec2.garantiadata.com',
                port=18592,
                password='kiran@cr7')

#everything releated to feed will be in this file
                
def place_sale(sale, locale):
    locale = locale.split(',').reverse()
    #the locality is from the locale list
    locality = locale[1]
    potential_users = []
    for user in User.objects.all():
        if user.locale.split(',')[1] == locality:
            #this user must see this sale object
            potential_users.append(user)
            
            
            
def generate_feed(user_id):
    user = User.objects.get(user_id=user_id)
    user_redis_key = user.redis_key
    user_locale = user.locale.split(',')
    user_locality = user_locale[1]
    return None