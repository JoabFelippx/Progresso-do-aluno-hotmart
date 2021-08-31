import requests
import json

# Credenciais Developers
CLIENT_ID = ''
CLIENT_SECRET = ''
BASIC = ''

url = 'https://api-sec-vlc.hotmart.com/security/oauth/token?grant_type=client_credentials&client_id=' + \
    CLIENT_ID + '&client_secret=' + CLIENT_SECRET

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + BASIC
}


# obter o seu access_token
def TOKEN_CB():
    get_token = requests.post(url, headers=headers)
    json = get_token.json()

    return json['access_token']