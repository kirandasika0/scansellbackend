from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home), 
    url(r'hh/', views.test_view),
]