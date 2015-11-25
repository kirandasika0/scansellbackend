from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home), 
    url(r'^insert_book/', views.insert_book),
]