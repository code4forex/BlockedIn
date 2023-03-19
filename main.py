import requests

# Set your access token
access_token = 'YOUR_ACCESS_TOKEN'

# Retrieve the authenticated member's ID
api_endpoint = 'https://api.linkedin.com/v2/me'
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(api_endpoint, headers=headers)
if response.status_code == 200:
    me_data = response.json()
    member_id = me_data['id']
else:
    print(f'Error retrieving authenticated member ID: {response.json()["message"]}')

# Set the member ID of the user you want to block
user_to_block_id = 'USER_TO_BLOCK_ID'

# Set the API endpoint to block the user
api_endpoint = f'https://api.linkedin.com/v2/people/{user_to_block_id}/relation-to-viewee?action=block'

# Send the API request to block the user
response = requests.post(api_endpoint, headers=headers)

# Check the response status code to confirm the user was blocked successfully
if response.status_code == 200:
    print(f'User {user_to_block_id} was blocked successfully.')
else:
    print(f'Error blocking user {user_to_block_id}: {response.json()["message"]}')
