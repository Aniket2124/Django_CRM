from django.contrib import admin
from django.urls import path
from .views import lead_list, lead_details, lead_create

urlpatterns = [
    
    path('',lead_list,name='lead_list'),
    path('lead_details/<int:pk>',lead_details,name='lead_detail'),
    path('lead-create',lead_create,name='lead_create')
]