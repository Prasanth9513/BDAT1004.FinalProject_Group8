# import requests

# url = "https://covid-193.p.rapidapi.com/statistics"

# headers = {
# 	"X-RapidAPI-Key": "eba8bf64c0msha8d7872eae06eccp147836jsn25ca06e40347",
# 	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)
import requests

url = "https://currencyscoop.p.rapidapi.com/historical"

querystring = {"date":"2022-02-05"}

headers = {
	"X-RapidAPI-Key": "eba8bf64c0msha8d7872eae06eccp147836jsn25ca06e40347",
	"X-RapidAPI-Host": "currencyscoop.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)