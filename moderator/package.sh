#!/bin/bash

rm -rf package
rm -f package.zip

mkdir package

# Install dependencies
pip install boto3 requests -t package/

# Copy moderator code
cp *.py package/

# Create zip package
(cd package && zip -r ../package.zip *) > /dev/null

echo "Package created: package.zip"
