from django.shortcuts import reverse, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from.mixins import organizerAndLoginRequiredMixin
from django.core.mail import send_mail
import random

# Create your views here.
class AgentListView(organizerAndLoginRequiredMixin, generic.ListView):  
   
    context_object_name = 'agent_list'
    template_name='agents/agent_list.html'
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organizations=organization)

class AgentCreateView(organizerAndLoginRequiredMixin, generic.CreateView):
    template_name= 'agents/create_agent.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0,100000)}")
        user.save()
        Agent.objects.create(user=user,organizations = self.request.user.userprofile)
        send_mail(

            subject ="You are to be Agent",
            message = "Welcome to DJCRM please login to start working.",
            from_email = "admin@dmin.com",
            recipient_list = [user.email]

        )
        # agent.organizations = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(organizerAndLoginRequiredMixin,generic.DetailView):
    template_name='agents/agent_details.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organizations=organization)

class AgentUpdateView(organizerAndLoginRequiredMixin, generic.UpdateView):
    form_class = AgentModelForm
    template_name='agents/agent_update.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        return Agent.objects.all()

class AgentDeleteView(organizerAndLoginRequiredMixin, generic.DeleteView):
    model = Agent
    template_name='agents/agent_delet.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organizations=organization)