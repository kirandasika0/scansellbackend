from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^create_user/', views.create_user),
    url(r'^location_update/', views.update_location),
]