from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^create_user/', views.SignupView.as_view()),
    url(r'^update_location/', views.update_location),
    url(r'login/', views.LoginView.as_view()),
    url(r'my_sales/', views.mySales),
    url(r'all_users/', views.allUsers),
]
