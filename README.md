It has two components:

* router - decides if it needs to invoke the second function
* reactor - the main logic 

It's split into two parts to work around Slack's 3 second timeout


First, deploy the router:

```bash
cd router
bash publish.sh
```

Next, deploy the reactor:

```bash
make deploy
```