# hibp
semiautomatic tool for data breach affected users 
## How?
Manually you need to go to haveibeenpwned.com website and request a breach result for tradeshift. COnfirmation is received via email and contain a token which need to be enteredon the website.
At this moment you have a latest breach information publicly available in a json format. This represent the input file for the script.

## Requirements
Python 2.7.17 - see python modules used in requirements.txt
OKTA token generated from application

## Install required modules
```
pip install -r requirements.txt
```

## Run the script
```
python script.py [Name_of_the_file].json
```

## Results
Opening the xlsx result file you can see which accounts are active in OKTA and need to be informed to change their account password.