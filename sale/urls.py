from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^new_sale/', views.new_sale),
    url(r'^title_case_string/', views.title_case_string),
    url(r'^new_sale_interest/', views.new_sale_interest),
    url(r'^new_sale_insert/', views.new_sale_insert),
    url(r'^redis_test/', views.redis_test),
    url(r'^create_locale/', views.create_locale),
    url(r'^get_feed/', views.get_feed),
    url(r'^new_get_feed/', views.new_get_feed),
]