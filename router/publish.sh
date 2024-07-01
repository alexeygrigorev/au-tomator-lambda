
FUNCTION_NAME="slack-test"


rm -rf package
rm package.zip

mkdir package

# pip install -r requirements.txt -t package/

cp *.py package
rm -f package/test*.py

(cd package && zip -r ../package.zip *) > /dev/null



CURRENT_DIR=${PWD}


if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    CURRENT_DIR=$(cygpath -w ${PWD})
fi


echo "Deploying to AWS Lambda..."


aws lambda \
    update-function-code \
    --function-name ${FUNCTION_NAME} \
    --zip-file fileb://${CURRENT_DIR}/package.zip \
        > /dev/null
