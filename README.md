

Preparing the package:

```python
bash package.sh
```

Upload it:

```python
aws lambda \
    update-function-code \
    --function-name slack-test \
    --zip-file fileb://`cygpath -w ${PWD}`/package.zip \
        > /dev/null
```

```bash
python -m venv venv
source venv/Scripts/activate
# source venv/bin/activate
pip install -r requirements.txt
python test_ai.py
```

