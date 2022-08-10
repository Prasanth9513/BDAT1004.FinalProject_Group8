from cgitb import lookup
from cmath import pi
from multiprocessing import context
from django.shortcuts import render,HttpResponse
import requests
from .models import Exchange
import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
# Create your views here.
from .serializers import ExchangeSerializer
from rest_framework.response import Response



def dashboard(request):
    if request.GET:
        context={}
        date=request.GET.get('getdate')
        ex=Exchange.objects.filter(response_date=date).values('item','rate')
        exchang_dict={}
        for i in ex:
            exchang_dict[i['item']]=i['rate']

        itemlist=list(exchang_dict.keys())
        ratelist=list(exchang_dict.values())

        context['itemlist']=itemlist
        context['ratelist']=ratelist
        context['base']="USD"
        context['date']=date
        return render(request,'application/dashboard.html',context)

    context={}
    today_date=datetime.datetime.today().date()
    ex=Exchange.objects.filter(response_date=today_date).values('item','rate')
    exchang_dict={}
    for i in ex:
        exchang_dict[i['item']]=i['rate']

    itemlist=list(exchang_dict.keys())
    ratelist=list(exchang_dict.values())

    context['itemlist']=itemlist
    context['ratelist']=ratelist
    context['base']="USD"
    context['date']=str(today_date)
    print(context['date'])
    return render(request,'application/dashboard.html',context)


def get_data(request):

    try: 
        url = "https://currencyscoop.p.rapidapi.com/historical"

        today_date=str(datetime.datetime.today().date())
        print(type(today_date),today_date)

        querystring = {"date":today_date}

        headers = {
            "X-RapidAPI-Key": "eba8bf64c0msha8d7872eae06eccp147836jsn25ca06e40347",
            "X-RapidAPI-Host": "currencyscoop.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        # print(response.json()['response']['date'])
        res_date=response.json()['response']['date']
        # print(response.json()['response']['base'])
        res_base=response.json()['response']['base']
        # print(response.json()['response']['rates'])
        res_rate=response.json()['response']['rates']
        print(response.json())
        # print('res_rate',res_rate)
        i=0
        for x,y in res_rate.items():
            if(i<30):
                d=Exchange(response_date=res_date,base=res_base,item=x,rate=float(y))
                d.save()
                i=i+1
        return HttpResponse("Data successfully added !")
        

    except:
        print('can not run get data in application view')
        return HttpResponse("Data not added !")

class CR_ExchangeApiView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=Exchange.objects.all()
    serializer_class=ExchangeSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def  post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

        
        
        

class U_ExchangeApiView(GenericAPIView,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin):
    queryset=Exchange.objects.all()
    serializer_class=ExchangeSerializer
    lookup_field="id"

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class Getbydate_ExchangeApiView(GenericAPIView):
    queryset=Exchange.objects.all()
    serializer_class=ExchangeSerializer
    def get(self,request,response_date=None):
        queryset            =   Exchange.objects.filter(response_date=response_date)
        # print(queryset)
        serialize           =   ExchangeSerializer(queryset,many=True,context={'request': request})
        # print(serialize.data)
        return Response(serialize.data)

class Getbyitem_ExchangeApiView(GenericAPIView):
    queryset=Exchange.objects.all()
    serializer_class=ExchangeSerializer
    def get(self,request,item=None):
        queryset            =   Exchange.objects.filter(item=item)
        # print(queryset)
        serialize           =   ExchangeSerializer(queryset,many=True,context={'request': request})
        # print(serialize.data)
        return Response(serialize.data)

class Getbydaterange_ExchangeApiView(GenericAPIView):
    queryset=Exchange.objects.all()
    serializer_class=ExchangeSerializer
    def get(self,request,fromdate=None,todate=None):
        # fromdate=self.request.GET.get('fromdate')
        # todate=self.request.GET.get('todate')
        print(fromdate,todate)
        queryset            =   Exchange.objects.filter(response_date__gte=fromdate,response_date__lte=todate)
        serialize           =   ExchangeSerializer(queryset,many=True,context={'request': request})
        return Response(serialize.data)


# import time
# import datetime
# Initiating = True
# print(datetime.datetime.now())
# while True:
#     if Initiating == True:
#         print("Initiate")
#         print( datetime.datetime.now())
#         time.sleep(60 - time.time() % 60+5)
#         Initiating = False
#     else:
#         time.sleep(60)
#         print("working")
#         print(datetime.datetime.now())

