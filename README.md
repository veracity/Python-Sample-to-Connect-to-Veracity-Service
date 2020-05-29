# Python IoT HUB example app

## About

The app is a skeleton application/sdk serving as a starting point for
authenticating and making calls to DNV GL's API.

The application uses Client Credentials with client secret
for authentication. AAD also provides a token cache with
an automatic renewal of expired tokens. Add session storage,
like Redis, for more persistent storage of tokens.

## Prerequisites

For using this example you need:

- Python 3+
- [Microsoft Authentication Library for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python) (MSAL)
- Your app registered with client id and client secret in our AAD.
  The client id also needs permission to the data in question.

## Setup

Install Microsoft Authentication Library (MSAL):

```
pip install msal
```

Install this SDK package with the script and config.json. Edit
config.json with the Client Credential information provided to you.

## Configuration

The configuration is in a separate file. The default file
is config.json. However, you can use any file you like. You can
provide the path as the first argument of the script:

```
python app.py .\path\to\another_config.json
```

These are the options in the config file:

- authority - tenant name in the form of "https://login.microsoftonline.com/TenantName" (e.g. name.onmicrosoft.com)
- client_id - the client id
- client_secret - the client secret
- scope - array with scopes, e.g. url ending with ".default"
- endpoint - endpoint to test that authentication is working

## A note on security

The configuration contains the client id and client secret in this
example to keep things simple.

In a real solution, you should implement a proper, secure way to
store and retrieve the client secret. Avoid having actual authentication
information in a file in a repro.

Instead, provide the client secret as an environment variable or
in a secure key vault.
