# How to auto-generate actions from Slack API

```shell
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
./generate_openapi.py
```

## How it works:

1) Grab the Slack OpenAPI spec from GitHub
2) Use the OpenAPI spec to give us a list of "methods"
3) The OpenAPI spec does NOT contain "default" values for parameters, so we need to get those from elsewhere
4) Goto the public HTTP API reference https://api.slack.com/methods and parse the HTML for the Default parameter values
5) Combine the "default" values from the HTTP API reference with the OpenAPI information
6) Render a Jinja template `template.jinja` with the combined data
7) Write the rendered Jinja template to `../actions/<method>.yaml`
