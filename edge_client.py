import os
import requests
from flask import Flask

app = Flask(__name__)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
map_server = os.getenv('MAP_SERVER_URL')
token_auth_url = "https://sso.smartabyarsmartvillage.org/auth/realms/SMARTVILLAGE/protocol/openid-connect/token"

token_auth_payload =  {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}
response = requests.post(token_auth_url, token_auth_payload)

access_token = ""
if response.status_code == 200:
    access_token = response.json().get('access_token')
    print(f"Token: {access_token}")
else:
    print(f"Status: {response.status_code}")

api_uri = "https://www.smartabyarsmartvillage.org"
map_data_api = "/api/map-result"
smart_traffic_light_api= "/api/smart-traffic-light-import"
map_data = ""
headers = {
    'Authorization': f'Bearer {access_token}',
}

def get_map_data():
    map_result = requests.get(url=api_uri+map_data_api, headers=headers)

    if map_result.status_code == 200:
        map_data = map_result.json()
        print(f"GET Request Successful. Data: {map_data}")
    else:
        print(f"GET Status code: {map_result.status_code}")

def update_data():
    light_data = {
    'operationId': 'putimportSmartTrafficLight',
        'x-vertx-event-bus': 'smartabyar-smartvillage-enUS-SmartTrafficLight',
        #'KEY from above data': 'value from get data',
    }
    put_response = requests.put(url=map_server+smart_traffic_light_api, data=light_data, headers=headers)

    if put_response.status_code == 201:
        # Process the response data for a successful POST request
        put_data = put_response.json()
        print(f"Successful PUT, Updated: {put_data}")
    else:
        print(f"PUT Failed: {put_response.status_code}, {put_response.text}")

@app.route('/health')
def check_data():
    get_map_data()
    #update_data()
    return "App is running"
