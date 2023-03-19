import requests
import webbrowser


# Set the LinkedIn OAuth 2.0 credentials
client_id = '86rxuhvq2icqqa'
client_secret = 'kj3AikdZ35zlu9cs'
redirect_uri = 'https://www.linkedin.com/developers/tools/oauth/redirect'
scope = 'r_liteprofile r_emailaddress'

# Construct the URL for the LinkedIn OAuth 2.0 authorization endpoint
authorization_endpoint = 'https://www.linkedin.com/oauth/v2/authorization'
authorization_url = f'{authorization_endpoint}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'

# Open the LinkedIn authentication popup in the user's web browser
openbrowser = webbrowser.open_new(authorization_url)

# Wait for the user to authenticate and grant authorization
authorization_code = input('Enter the authorization code: ')

# Exchange the authorization code for an access token
token_endpoint = 'https://www.linkedin.com/oauth/v2/accessToken'
token_params = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret
}
response = requests.post(token_endpoint, data=token_params)
if response.status_code == 200:
    access_token = response.json()['access_token']
    print(f'Access token: {access_token}')
else:
    print(f'Error: {response.json()["error_description"]}')
