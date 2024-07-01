#!/bin/bash

FUNCTION_NAME="automator-process-reaction"
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
