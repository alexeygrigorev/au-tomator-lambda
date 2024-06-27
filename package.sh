
rm -rf package
rm package.zip

mkdir package

LOCAL_PATH=`cygpath -w ${PWD}`
echo ${LOCAL_PATH}

docker run --rm \
    -v .:/var/task \
    -w /var/task \
    amazon/aws-lambda-python:3.12 \
    pip install -r requirements.txt -t package/

cp lambda_function.py package

(cd package && zip -r ../package.zip *) > /dev/null

