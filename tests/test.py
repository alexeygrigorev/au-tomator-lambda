import json

with open('event.json') as f_in:
    event = json.load(f_in) 

import lambda_function
lambda_function.lambda_handler(event, None)