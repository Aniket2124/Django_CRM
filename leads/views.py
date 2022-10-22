from multiprocessing import context
from django.shortcuts import render, redirect,reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Category, Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import organizerAndLoginRequiredMixin


class HomeView(TemplateView):
    template_name="landing.html"


# def home(request):
#     return render(request,"landing.html")

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name='registration/signup.html'

    def get_success_url(self):
        return reverse ("login")


# Create your views here.
def lead_list(request):
    data = Lead.objects.all()
    context = {"data":data}
    return render(request,"leads/lead_list.html", context)


#---------------------------
class LeadListView(LoginRequiredMixin, ListView):
    context_object_name = 'data'
    template_name='leads/lead_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organizations = user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organizations = user.agent.organizations, agent__isnull=False)
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organizations = user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads":queryset
            })
        return context


def lead_details(request, pk):
    lead = Lead.objects.get(id=pk)
    return render(request,"leads/lead_details.html", {"lead":lead})
#-------------------------------
class LeadDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'lead'
    template_name='leads/lead_details.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organizations = user.userprofile)
        else:
            queryset = Lead.objects.filter(organizations = user.agent.organizations)
            queryset = queryset.filter(agent__user = user)
        return queryset

# def lead_create(request):
    # form = LeadForm() 
    # if request.method == "POST":
    #     print("Post request")
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         print(" Form is valid")
    #         print(form.cleaned_data)
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         lead = Lead.objects.create(first_name=first_name, last_name=last_name, age=age, agent=agent)
    #         # lead.save()
    #         return redirect("/")

    # context={
    #     "form":LeadForm()
    # }
#     return render(request,"leads/create_lead.html",context)
    
    
def lead_create(request):
    form = LeadModelForm() 
    if request.method == "POST":
        print("Post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():            
            form.save()
            return redirect("/")

    context={
        "form":LeadModelForm()
    }
    return render(request,"leads/create_lead.html",context)
    #-----------------------------------

class LeadCreateView(organizerAndLoginRequiredMixin, CreateView):
    # model = Lead
    # context_object_name = 'lead'
    form_class = LeadModelForm
    template_name='leads/create_lead.html'

    def get_success_url(self):
        return reverse ("leads:lead_list")


    def form_valid(self,form) :
        lead = form.save(commit=False)
        lead.organizations = self.request.user.userprofile
        lead.save()
        # to send email
        send_mail(
            subject = "Lead has been Created",
            message= "Go to the site to see new lead.",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm() 
#     if request.method == "POST":
#         print("Post request")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print(" Form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name=first_name
#             lead.last_name=last_name
#             lead.age=age
#             lead.save()
#             return redirect("/")

#     context={
#         "form":LeadForm()
#     }
#     return render(request,"leads/update_lead.html",context)



def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead) 
    if request.method == "POST":
        print("Post request")
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():            
            form.save()
            return redirect("/")

    context={
        "form":LeadModelForm(),
        "lead":lead
    }
    return render(request,"leads/update_lead.html",context)

#--------------------------------------
class LeadUpdateView(organizerAndLoginRequiredMixin, UpdateView):
    form_class = LeadModelForm
    template_name='leads/update_lead.html'

    def get_queryset(self):
        user = self.request.user       
        return Lead.objects.filter(organizations = user.userprofile)

    def get_success_url(self):
        return reverse ("leads:lead_list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/")

#---------------------------------
class LeadDeleteView(organizerAndLoginRequiredMixin, DeleteView):
    model = Lead
    template_name='leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user       
        return Lead.objects.filter(organizations = user.userprofile)

    def get_success_url(self):
        return reverse ("leads:lead_list")


class AssignAgentView(organizerAndLoginRequiredMixin ,FormView):
    template_name='leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update( {
            "request":self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse ("leads:lead_list")

    def form_valid(self,form) :
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name='leads/category_list.html'
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Lead.objects.filter(organizations = user.userprofile)
        else:
            queryset = Lead.objects.filter(organizations = user.agent.organizations)           
        


        context.update({
            "unassigned_lead_count":queryset.filter(category__isnull = True).count()
        })
        return context



    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(organizations = user.userprofile)
        else:
            queryset = Category.objects.filter(organizations = user.agent.organizations)
            
        return queryset

    
class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name='leads/category_detail.html'
    context_object_name = "category"

    # def get_context_data(self, **kwargs):        
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()


    #     context.update({
    #         "leads":leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(organizations = user.userprofile)
        else:
            queryset = Category.objects.filter(organizations = user.agent.organizations)
            
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    form_class = LeadCategoryUpdateForm
    template_name='leads/lead_category_update.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organizations = user.userprofile)
        else:
            queryset = Lead.objects.filter(organizations = user.agent.organizations)
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_success_url(self):
        return reverse ("leads:lead_detail", kwargs={"pk":self.get_object().id})