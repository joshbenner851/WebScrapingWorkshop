import requests
import json

url = "http://www.connectedin.io/users"
headers_dict = {'User-Agent': 'Mozilla/5.0',"Content-Type":"application/json"}
# headers_dict = {'User-Agent': 'Mozilla/5.0'}

# Send the request to grab the data
response = requests.get(url, headers=headers_dict)

print("Status code", response.status_code)

# Convert the response into json and set it to the data
data = response.json()
print(data)

user = {
            "_id": "5818cedcafaaf221321383fb",
            "formattedName": "Parker Dodson",
            "id": "R4CobbFkS7",
            "publicProfileUrl": "https://www.linkedin.com/in/parker-dodson-598908a9",
            "__v": 0,
            "positions": {
                "values": [
                    {
                        "id": 850277883,
                        "isCurrent": "true",
                        "summary": "A Lab assistant for the lab section of ECE 345 (Electronic Instrumentation and Systems). Where I Help students trouble shoot their projects. ",
                        "title": "Undergraduate Lab Assistant",
                        "lat": 42.7369792,
                        "long": -84.48386540000001,
                        "_id": "5818cedcafaaf221321383fc",
                        "location": {
                            "name": "East Lansing, Michigan"
                        },
                        "company": {
                            "name": "Michigan State University. Department of Electrical and Computer Engineering"
                        }
                    }
                ]
            },
            "location": {
                "name": "Lansing, Michigan Area",
                "country": {
                    "code": "us"
                }
            }
        }

postresponse = requests.post('http://connectedin.io/users', data=user)
print(postresponse.status_code)

water_data = requests.get('https://api.fitbit.com/1/user/-/profile.json',{
# "access_token":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0V0IzUlIiLCJhdWQiOiIyMjgyR1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTA2NDU5NjY0LCJpYXQiOjE1MDU4NjY3MTJ9.NXZb4ktXr4vOLt6q5xsz2cs_MzJjcIWR-3g6zfeqpAg",
"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0V0IzUlIiLCJhdWQiOiIyMjdHNUwiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3bnV0IiwiZXhwIjoxNTA1OTQxNjAzLCJpYXQiOjE1MDU4NTUyMDN9.Swh9-9c8jk68CwZru7jvig7CFrgUJYXZFGz2c7uDK_A"})

print("water_data: ", water_data)

fitbit_response = requests.post('https://api.fitbit.com/1/user/4WB3RR/foods/log/water.json',{'amount': '500', 'date':'2017-09-19'})

print(fitbit_response)


