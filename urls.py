from django.conf.urls import url
from django.urls import path
from projekt47 import views

urlpatterns = [
    path('', views.index),
    path('addons/', views.addons),
    #url(r'^parser/', include('mensaparser.urls')),
    #path('kicken/', include('kicken.urls')),
]
