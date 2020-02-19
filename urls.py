from django.conf.urls import url
from django.urls import path
from projekt47 import views

urlpatterns = [
    path('', views.index),
    path('addons/', views.addons),
    path('addons/<addon_id>/', views.addon),
    path('charaktere/', views.characters),
    path('charaktere/<char_id>/', views.character),
    #url(r'^parser/', include('mensaparser.urls')),
    #path('kicken/', include('kicken.urls')),
]
