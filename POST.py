import requests
import json

url = 'https://192.168.1.72:5000/api/notification'
data = {'key1': 'value1', 'key2': 'value2'}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)
print(response.json())