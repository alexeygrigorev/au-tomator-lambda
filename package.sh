rm -rf package
rm package.zip

mkdir package

pip install -r requirements.txt -t package/

cp automator/* package

(cd package && zip -r ../package.zip *) > /dev/null

