import requests
import json

with open('event.json') as f_in:
    event = json.load(f_in) 

# import lambda_function
# lambda_function.lambda_handler(event, None)

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

response = requests.post(url, json=event)