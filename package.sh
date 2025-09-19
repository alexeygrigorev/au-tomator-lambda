rm -rf package
rm package.zip

mkdir package

uv pip install -r requirements.txt --target package/

cp automator/* package

(cd package && zip -r ../package.zip *) > /dev/null

