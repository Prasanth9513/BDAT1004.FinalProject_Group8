from django_cron import CronJobBase, Schedule
from .models import Exchange
import requests
import datetime

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 24*60*60 # every 24 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.my_cron_job'  

    def do(self):
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
        # print(response.json())
        # print('res_rate',res_rate)
        i=0
        for x,y in res_rate.items():
            if(i<30):
                d=Exchange(response_date=res_date,base=res_base,item=x,rate=float(y))
                d.save()
                i=i+1
        

      except:
        print('can not run get data in application view')


# */1 * * * * source /home/satish/.bashrc && source /home/satish/taran_django_project/Project1/project1/bin/activate && python home/satish/taran_django_project/Project1/project1/manage.py runcrons > /home/satish/cronjob.log