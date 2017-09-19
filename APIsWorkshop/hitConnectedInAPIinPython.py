import requests
import json

url = "http://www.connectedin.io/users"
headers_dict = {'User-Agent': 'Mozilla/5.0',"Content-Type":"application/json"}
# headers_dict = {'User-Agent': 'Mozilla/5.0'}

# Send the request to grab the data
response = requests.get(url, headers=headers_dict)

data = response.json()
print(data)