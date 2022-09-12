
FUNCTION_NAME="slack-test"
BUILD_PATH=`cygpath -w ${PWD}`/package.zip

aws lambda update-function-code \
    --function-name ${FUNCTION_NAME} \
    --zip-file fileb://${BUILD_PATH}