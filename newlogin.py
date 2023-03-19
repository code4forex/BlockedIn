import requests
import webbrowser
import jwt


# Set the LinkedIn OAuth 2.0 credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'YOUR_REDIRECT_URI'
scope = 'r_liteprofile r_emailaddress openid'

# Construct the URL for the LinkedIn OAuth 2.0 authorization endpoint
authorization_endpoint = 'https://www.linkedin.com/oauth/v2/authorization'
authorization_url = f'{authorization_endpoint}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'

# Open the LinkedIn authentication popup in the user's web browser
openbrowser = webbrowser.open_new(authorization_url)

# Wait for the user to authenticate and grant authorization
authorization_code = input('Enter the authorization code: ')

# Exchange the authorization code for an access token and ID token
token_endpoint = 'https://www.linkedin.com/oauth/v2/accessToken'
token_params = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret,
}
token_response = requests.post(token_endpoint, data=token_params)
if token_response.status_code == 200:
    token_data = token_response.json()
    access_token = token_data['access_token']
    id_token = token_data['id_token']
else:
    print(f'Error retrieving access token: {token_response.json()["error_description"]}')

# Retrieve the discovery document URL from the access token metadata
metadata_endpoint = 'https://api.linkedin.com/v2/oauth2/accessTokenMetadata'
metadata_headers = {'Authorization': f'Bearer {access_token}'}
metadata_response = requests.get(metadata_endpoint, headers=metadata_headers)
if metadata_response.status_code == 200:
    metadata_data = metadata_response.json()
    discovery_document_url = metadata_data['issuer'].replace('/oauth2', '') + '/.well-known/openid-configuration'
else:
    print(f'Error retrieving access token metadata: {metadata_response.json()["message"]}')

# Retrieve the discovery document
discovery_response = requests.get(discovery_document_url)
if discovery_response.status_code == 200:
    discovery_document = discovery_response.json()
    jwks_uri = discovery_document['jwks_uri']
else:
    print(f'Error retrieving discovery document: {discovery_response.json()["error_description"]}')

# Retrieve the JSON Web Key Set (JWKS) from the jwks_uri
jwks_response = requests.get(jwks_uri)
if jwks_response.status_code == 200:
    jwks = jwks_response.json()
else:
    print(f'Error retrieving JSON Web Key Set: {jwks_response.json()["error_description"]}')

# Decode the ID token and extract the member details
decoded_id_token = jwt.decode(id_token, jwks, algorithms=['RS256'], audience=client_id, issuer='https://www.linkedin.com')
member_id = decoded_id_token['sub']
member_name = decoded_id_token['name']
member_given_name = decoded_id_token['given_name']
member_family_name = decoded_id_token['family_name']
member_picture = decoded_id_token['picture']
member_locale = decoded_id_token['locale']
member_email = decoded_id_token['email']
member_email_verified = decoded_id_token['email_verified']

# Call the userinfo endpoint to retrieve the member details
userinfo_endpoint = 'https://api.linkedin.com/v2/userinfo'
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(userinfo_endpoint, headers=headers)

# Check the response status code and retrieve
if response.status_code == 200:
userinfo_data = response.json()
member_id = userinfo_data['sub']
member_name = userinfo_data['name']
member_given_name = userinfo_data['given_name']
member_family_name = userinfo_data['family_name']
member_picture = userinfo_data['picture']
member_locale = userinfo_data['locale']
member_email = userinfo_data['email']
member_email_verified = userinfo_data['email_verified']
else:
print(f'Error retrieving member profile: {response.json()["message"]}')

# Print out the retrieved member details
print(f'Member ID: {member_id}')
print(f'Member Name: {member_name}')
print(f'Member Given Name: {member_given_name}')
print(f'Member Family Name: {member_family_name}')
print(f'Member Picture: {member_picture}')
print(f'Member Locale: {member_locale}')
print(f'Member Email: {member_email}')
print(f'Member Email Verified: {member_email_verified}')
