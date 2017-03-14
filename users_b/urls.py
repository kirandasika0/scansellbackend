from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^create_user/', views.signUpUser),
    url(r'^update_location/', views.update_location),
    url(r'login/', views.login),
    url(r'my_sales/', views.mySales),
    url(r'all_users/', views.allUsers),
]
