

Preparing the package:

```python
bash package.sh
```

Upload it:

```python
aws lambda \
    update-function-code \
    --function-name slack-test \
    --zip-file fileb://`cygpath -w ${PWD}`/package.zip
```

