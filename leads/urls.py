from django.contrib import admin
from django.urls import path

# from .views import lead_list,lead_details,lead_create,lead_update,lead_delete
from .views import LeadDeleteView, LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, DeleteView

app_name = "leads"
urlpatterns = [
    #function based urls
    # path('lead-list',lead_list,name='lead_list'),
    # path('lead-details/<int:pk>',lead_details,name='lead_detail'),
    # path('lead-create',lead_create,name='lead_create'),
    # path('lead_update/<int:pk>',lead_update,name='lead_update'),
    # path('lead-delete/<int:pk>',lead_delete,name='lead_delete'),

    #class based urls
    path('lead-list',LeadListView.as_view(),name='lead_list'),
    path('lead-details/<int:pk>',LeadDetailView.as_view(),name='lead_detail'),
    path('lead-create',LeadCreateView.as_view(),name='lead_create'),
    path('lead_update/<int:pk>',LeadUpdateView.as_view(),name='lead_update'),
    path('lead-delete/<int:pk>',LeadDeleteView.as_view(),name='lead_delete'),
   
]