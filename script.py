import sys
import requests
from progress.bar import Bar
from time import sleep
from datetime import datetime
import json
import pandas
from json.decoder import JSONDecoder
from glom import glom
from pprint import pprint
from dateutil import parser
from termcolor import colored
final_json = []
#GET request to haveibeenpwned with hibp-api-key
tstamp = datetime.now()
tstamp = tstamp.replace(day=1, hour=1, minute=1)
currenttime = tstamp.strftime("%Y-%m-%dT%H:%M:%SZ")
#read token-API for OKTA from file
token_file = open("OKTAtoken-API.txt","rb")
oktatoken_API = token_file.read().splitlines()
#print(str(oktatoken_API[0]))
print("Verifying current breaches occured after: "+ currenttime)
token_file.close()
#for testing: 
#with open('anothertest.json') as json_file:
#open input file to read the json from haveibeenpwned
print("Open file as input: "+sys.argv[1])
with open(sys.argv[1]) as json_file:
    data = json.load(json_file)
#    print(len(data["BreachSearchResults"]))
#TO-DO make a running status for current position out of total number
    bar = Bar('Processing', max=len(data["BreachSearchResults"]))
    for user in data["BreachSearchResults"]:
#        print(user["Alias"])
#        print("{}".format(len(user["Breaches"])) + " breaches occured")
        bar.next()
        for breach in user["Breaches"]:
#if breach occure later than begining of last month than put the record in a file
            #if breach["AddedDate"] > currenttime :
            if breach["AddedDate"] > "2019-10-16T00:00:00Z":
                #print(breach["Name"])
                #print(breach["AddedDate"])
                #print(colored("reset the password", 'red'))
#verify if the affected user is a current TS employee
                headers = {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': str(oktatoken_API[0]),
                        }
                params = (
                        ('q', user["Alias"]+"@"+user["DomainName"]),
                        )
                response = requests.get('https://tradeshift.okta.com/api/v1/users', headers=headers, params=params)
                #print(user["Alias"]+"@"+user["DomainName"])
                #print("OKTA query response length: ")
                #print(len(response.json()))
                user_exist = 0
                if len(response.json()) > 0 : user_exist = 1
                #f.write(user["Alias"])
                #f.write('\n')
                #f.write(breach["Name"])
                #f.write('\n')
                #f.write('\n')
                final_json.append({"active in OKTA": user_exist, "user": user["Alias"]+"@"+user["DomainName"], "BreachName": breach["Name"], "BreachDate": breach["BreachDate"], "BreachTitle": breach["Title"]})
print
print(tstamp)
print
bar.finish()
fjson = open("jsonformat.json","wb")
fjson.write(json.dumps(final_json, indent = 5, sort_keys=True))
fjson.close()
print("Converting json to xlsx")
pandas.read_json("jsonformat.json").to_excel("toreset.xlsx")
print("Number of records: ")
print(len(final_json))
print("Exported file: toreset.xlsx")
