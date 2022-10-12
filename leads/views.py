from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead

# Create your views here.
def home(request):
    data = Lead.objects.all()
    context = {"data":data}
    return render(request,"leads/index.html", context)

