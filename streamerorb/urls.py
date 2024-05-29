from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_image/', views.get_image, name='get_image')
]