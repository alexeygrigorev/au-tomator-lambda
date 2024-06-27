FROM amazon/aws-lambda-python:3.12

# COPY package /var/task/

RUN pip install requests groq pydantic
COPY lambda_function.py lambda_function.py

CMD ["lambda_function.lambda_handler"]