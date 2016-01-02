from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^create_user/', views.create_user),
]