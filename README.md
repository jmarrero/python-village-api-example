# python-village-api-example
We are building a small python microservice that talks to the smart village api.

First we need to import two packages 
1) requests which we will use to talk to the API via HTTP.
2) os which we will use to get the credentials from environment variables.

```
import os
import requests
```

A common authentication pattern is gathering a access token, then using that access token from that moment on to do requests to the API.

On the first section of the code we want to get that access token. For that we will need the Client ID, Client Secret and the http endpoint the Autenthication server is located at. For that reason we are going to define it on the code. 
Since we don't want to hardcode credentials we will read these from environment variables.

```
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
token_auth_url = "https://sso.smartabyarsmartvillage.org/auth/realms/SMARTVILLAGE/protocol/openid-connect/token"
```
