from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead
from .forms import LeadForm

# Create your views here.
def lead_list(request):
    data = Lead.objects.all()
    context = {"data":data}
    return render(request,"leads/lead_list.html", context)

def lead_details(request, pk):
    lead = Lead.objects.get(id=pk)
    return render(request,"leads/lead_details.html", {"lead":lead})

def lead_create(request):
    context={
        "form":LeadForm()
    }
    return render(request,"leads/create_lead.html",context)
    
    