from django.contrib import admin
from django.urls import path
from .views import lead_list, lead_details, lead_create, lead_update, lead_delete


app_name = "leads"
urlpatterns = [
    
    path('',lead_list,name='lead_list'),
    path('lead-details/<int:pk>',lead_details,name='lead_detail'),
    path('lead-create',lead_create,name='lead_create'),
    path('lead_update/<int:pk>',lead_update,name='lead_update'),
    path('lead-delete/<int:pk>',lead_delete,name='lead_delete')
]