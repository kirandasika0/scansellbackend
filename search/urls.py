from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'hh/', views.test),
    url(r'^$', views.home), 
]