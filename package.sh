
rm -rf package
rm package.zip

mkdir package

pip install requests==2.28.1 -t package
cp lambda_function.py package

(cd package && zip -r ../package.zip *) > /dev/null

