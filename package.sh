
rm -rf package
rm package.zip

mkdir package

# docker run --rm \
#     -v .:/var/task \
#     -w /var/task \
#     amazon/aws-lambda-python:3.12 \
pip install -r requirements.txt -t package/

cp *.py package
rm -f package/test*.py

(cd package && zip -r ../package.zip *) > /dev/null

