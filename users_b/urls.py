from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^create_user/', views.signUpUser),
    url(r'^update_location/', views.update_location),
    url(r'login/', views.login),
]