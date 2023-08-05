# example/views.py
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from fcs.models import FundCompany, Issuer, Filling

import requests
import json
from types import SimpleNamespace

quarter_list = ['Q2 2023','Q1 2023','Q4 2022', 'Q3 2022', 'Q2 2022', 'Q1 2022', 'Q4 2021', 'Q3 2021', 'Q2 2021', 'Q1 2021', 'Q4 2020', 'Q3 2020', 'Q2 2020', 'Q1 2020', 'Q4 2019', 'Q3 2019', 'Q2 2019', 'Q1 2019', 'Q4 2018', 'Q3 2018']

def index(request):
   fund_companies = FundCompany.objects.all()
   issuers = Issuer.objects.all()
   return render(request, "index.html", {'fund_companies': fund_companies, 'issuers': issuers})

def manager(request, slug):
   quart = request.GET.get('q')
   fund_company = FundCompany.objects.get(cik_id = slug)

   data = {}
   hasdata = False
   # Crash on Server, Works on Local
   # try:
   #    url = f"https://data.sec.gov/submissions/CIK{slug}.json"
   #    response = requests.get(url, headers={"User-Agent": request.META['HTTP_USER_AGENT']})
   #    textResponse = response.text
   #    data = json.loads(textResponse, object_hook=lambda d: SimpleNamespace(**d))
   #    hasdata = True
   # except:
   #    print("crash")

   positions = Filling.objects.filter(cik_id = slug)
   positions_list = []
   for x in positions:
      cusip = x.cusip
      issuer = Issuer.objects.get(cusip = x.cusip).name
      ticker = Issuer.objects.get(cusip = x.cusip).ticker
      value = x.value
      shares = x.shares.replace("SH", "").replace("PRN", "")
      date = x.quarter_info
      dater = datetime.strptime(date, "%m-%d-%Y")
      quarter = assign_quarter(dater)
      positions_list.append(ManagerPositionsView(cusip, issuer,ticker, value, shares, date, quarter))
   
   if((quart is None) == False):
         quart = str(quart).replace("%", " ")
         if(quart != ""):
            positions_list = [value for value in positions_list if value.quarter == quart]
   else:
      quart = "All Quarters"  

   shares_data = [['Issuer', 'Shares']]
   for p in positions_list:
      shares_data.append([p.issuer, int(float(p.shares))])               

   return render(request, 'manager.html', {'fund_company': fund_company, 
                                           'data': data, 'hasdata': hasdata, 
                                           'positions' : positions_list, 
                                           'quarters' : quarter_list,
                                           'quart': quart,
                                           'shares_data': shares_data})

def issuer(request, slug):
   quart = request.GET.get('q')
   issuer = Issuer.objects.get(cusip = slug)

   positions = Filling.objects.filter(cusip = slug)
   positions_list = []
   for x in positions:
      cik = x.cik_id
      manager = FundCompany.objects.get(cik_id = x.cik_id).name
      value = x.value
      shares = x.shares.replace("SH", "").replace("PRN", "")
      date = x.quarter_info
      dater = datetime.strptime(date, "%m-%d-%Y")
      quarter = assign_quarter(dater)
      positions_list.append(IssuerPositionsView(cik, manager, value, shares, date, quarter))

   if((quart is None) == False):
      quart = str(quart).replace("%", " ")
      if(quart != ""):
         positions_list = [value for value in positions_list if value.quarter == quart]
   else:
      quart = "All Quarters"

   shares_data = [['Manager', 'Shares']]
   for p in positions_list:
      shares_data.append([p.manager, int(float(p.shares))])         
   
   return render(request, 'issuer.html', {'issuer': issuer, 
                                          'positions' : positions_list, 
                                          'quarters' : quarter_list,
                                          'quart': quart,
                                          'shares_data': shares_data})


class IssuerPositionsView:
   def __init__(self, cik, manager, value, shares, date, quarter):
    self.cik = cik
    self.manager = manager
    self.value = value
    self.shares = shares
    self.date = date
    self.quarter = quarter

class ManagerPositionsView:
   def __init__(self, cusip, issuer, ticker, value, shares, date, quarter):
    self.cusip = cusip
    self.issuer = issuer
    self.ticker = ticker
    self.value = value
    self.shares = shares
    self.date = date
    self.quarter = quarter    

def assign_quarter(date):
   month = date.month
   year = date.year
   if month in [1, 2, 3]:
      return "Q1 " + str(year)
   elif month in [4, 5, 6]:
      return "Q2 " + str(year)
   elif month in [7, 8, 9]:
      return "Q3 " + str(year)
   else:
      return "Q4 " + str(year)