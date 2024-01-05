import os
import requests
from flask import Flask

app = Flask(__name__)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
map_server = os.getenv('MAP_SERVER_URL')
token_auth_url = "https://sso.smartabyarsmartvillage.org/auth/realms/SMARTVILLAGE/protocol/openid-connect/token"

if client_id is None or client_secret is None:
    print("No CLIENT_ID or CLIENT_SECRET environment variable or defined...Exiting")
    exit(1)

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
map_data_api = "/api/map-result?rows=100&fq=dateTime:2024-02-29T13%3A59%3A58.000[America%2FNew_York]"
smart_traffic_light_api= "/api/smart-traffic-light-import"

def get_map_data():
    headers = {
    'Authorization': f'Bearer {access_token}',
    }
    map_result = requests.get(url=api_uri+map_data_api, headers=headers)

    if map_result.status_code == 200:
        map_data = map_result.json()
        print("GET Request Successful.")
    #    print(f"GET Request Successful. Data: {map_data}")
    else:
        print(f"GET Status code: {map_result.status_code}")
    return map_data

def update_data(map_data):
    headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    }

    all_coordinates = []
    for item in map_data['list']:
        if 'location' in item and 'coordinates' in item['location']:
            coordinates = item['location']['coordinates']
            all_coordinates.append(coordinates)

    light_data = {
        "pk": "veberod-intersection-1",
        "saves": ["entityId", "smartTrafficLightName", "location", "areaServed"],
        "entityId": "urn:ngsi-ld:SmartTrafficLight:SmartTrafficLight-veberod-intersection-1",
        "smartTrafficLightName": "Veberöd intersection 1",
        "location": {
            "type": "Point",
            "coordinates": []
        },
        "areaServed": [
        ]
    }

    light_data['location']['coordinates'] = all_coordinates[0] if all_coordinates else []
    light_data['areaServed'] = [{"type": "Point", "coordinates": coordinates} for coordinates in all_coordinates[1:]]

    if map_server is not None:
        put_response = requests.put(url=map_server+smart_traffic_light_api, data=light_data, headers=headers)
        if put_response.status_code == 201:
            put_data = put_response.json()
            print(f"Successful PUT, Updated: {put_data}")
        else:
            print(f"PUT Failed: {put_response.status_code}, {put_response.text}")
    else:
        print("No MAP_SERVER_URL environment variable defined")
        print("Printing payload to terminal:")
        print(light_data)

@app.route('/health')
def check_data():
    map_data = get_map_data()
    update_data(map_data)
    return "App is running"
