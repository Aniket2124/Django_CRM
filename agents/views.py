from django.shortcuts import reverse, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm

# Create your views here.
class AgentListView(LoginRequiredMixin, generic.ListView):
    model = Agent
    context_object_name = 'agent_list'
    template_name='agents/agent_list.html'
    def get_queryset(self):
        return Agent.objects.all()

class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name= 'agents/create_agent.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organizations = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(LoginRequiredMixin,generic.DetailView):
    template_name='agents/agent_details.html'
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.all()

class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = AgentModelForm
    template_name='agents/agent_update.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        return Agent.objects.all()

class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Agent
    template_name='agents/agent_delet.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_success_url(self):
        return reverse("agents:agent_update")