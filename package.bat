@echo off

REM Remove existing package directory and ZIP file
rmdir /s /q package
del package.zip

REM Create a new package directory
mkdir package

REM Convert the current directory to a Docker-friendly path
for /f "delims=" %%i in ('cd') do set CURRENT_DIR=%%i
for /f "delims=" %%i in ('cd') do set LOCAL_PATH=%%i

REM Echo the local path
echo %LOCAL_PATH%

REM Run Docker to install dependencies
docker run --rm ^
    -v %cd%:/var/task ^
    -w /var/task ^
    --entrypoint /bin/sh ^
    amazon/aws-lambda-python:3.12 ^
    -c "pip install -r requirements.txt -t package/"

REM Copy the Lambda function into the package directory
copy lambda_function.py package\

REM Create the deployment package
cd package
powershell Compress-Archive -Path * -DestinationPath ..\package.zip
cd ..


