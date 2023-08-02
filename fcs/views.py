# example/views.py
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from fcs.models import FundCompany

def index(request):
   fund_companies = FundCompany.objects.all()
   return render(request, "index.html", {'fund_companies': fund_companies})