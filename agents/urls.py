import imp
from django.urls import path
from .views import AgentListView, AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent_list'),
    path('create-agent', AgentCreateView.as_view(), name='create_agent'),
    path('agent-detail/<int:pk>/', AgentDetailView.as_view(), name='agent_detail'),
    path('agent-update/<int:pk>/', AgentUpdateView.as_view(), name='agent_update'),
    path('agent-delete/<int:pk>/', AgentDeleteView.as_view(), name='agent_delete')
    
]