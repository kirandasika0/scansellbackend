# This file will hold all the notification function to get and set notificaitions
from exceptions import NotificationNotFoundException
from .models import SaleNotification

def get_notif(notif_id):
    try:
        notification = SaleNotification.objects.get(pk=notif_id)
    except (SaleNotification.DoesNotExist):
        raise NotificationNotFoundException("Looks like the exception was not found")
    
    return serializers.serialize("json", [notification])[1:-1]