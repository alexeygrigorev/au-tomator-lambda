

Preparing the package:

```
bash package.sh
```

Upload it:

```
aws lambda \
    update-function-code \
    --function-name slack-test \
    --zip-file fileb://`cygpath -w ${PWD}`/package.zip
```

