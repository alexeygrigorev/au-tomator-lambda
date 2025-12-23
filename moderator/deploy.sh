#!/bin/bash

FUNCTION_NAME="automator-message-moderator"
CURRENT_DIR=${PWD}

if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    CURRENT_DIR=$(cygpath -w ${PWD})
fi

echo "Deploying Message Moderator to AWS Lambda..."

aws lambda \
    update-function-code \
    --function-name ${FUNCTION_NAME} \
    --zip-file fileb://${CURRENT_DIR}/package.zip \
        > /dev/null

echo "Deployment complete!"
