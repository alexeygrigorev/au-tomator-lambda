FROM amazon/aws-lambda-python:3.12

COPY package /var/task/
    
CMD ["lambda_function.lambda_handler"]