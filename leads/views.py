from django.shortcuts import render, redirect,reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

class HomeView(TemplateView):
    template_name="landing.html"


# def home(request):
#     return render(request,"landing.html")


# Create your views here.
def lead_list(request):
    data = Lead.objects.all()
    context = {"data":data}
    return render(request,"leads/lead_list.html", context)


#---------------------------
class LeadListView(ListView):
    model = Lead
    context_object_name = 'data'
    template_name='leads/lead_list.html'

def lead_details(request, pk):
    lead = Lead.objects.get(id=pk)
    return render(request,"leads/lead_details.html", {"lead":lead})
#-------------------------------
class LeadDetailView(DetailView):
    model = Lead
    context_object_name = 'lead'
    template_name='leads/lead_details.html'

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

class LeadCreateView(CreateView):
    # model = Lead
    # context_object_name = 'lead'
    form_class = LeadModelForm
    template_name='leads/create_lead.html'

    def get_success_url(self):
        return reverse ("leads:lead_list")


    def form_valid(self,form) :
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
class LeadUpdateView(UpdateView):
    model = Lead
    # context_object_name = 'lead'
    form_class = LeadModelForm
    template_name='leads/update_lead.html'

    def get_success_url(self):
        return reverse ("leads:lead_list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/")

#---------------------------------
class LeadDeleteView(DeleteView):
    model = Lead
    template_name='leads/lead_delete.html'

    def get_success_url(self):
        return reverse ("leads:lead_list")
