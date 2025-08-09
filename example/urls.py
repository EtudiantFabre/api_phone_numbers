# example/urls.py
from django.urls import path

from example.views import index, PhoneInfoView


urlpatterns = [
    path('', index, name='index'),
    path('phone-info/', PhoneInfoView.as_view(), name='phone-info'),
]