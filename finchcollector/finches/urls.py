from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('about/', views.about, name='about'),
    path('finches/', views.finches_index, name='index')
]

