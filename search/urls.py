from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'hh/', views.test_view),
   # url(r'^$', views.home), 
]