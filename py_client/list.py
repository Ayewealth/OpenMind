import requests
from getpass import getpass

endpoint = "http://127.0.0.1:8000/users"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5OTM1MzI1LCJpYXQiOjE2ODk5MzUwMjUsImp0aSI6ImQ1NGUzOWNmODY1MDQ1ZmU4ZDIyMDkwOTk0NTEwMGZmIiwidXNlcl9pZCI6MX0.2Bdrn9H25QPWPKnRo8r34SwL4bRA0bPOKnSgwv5i-Jw"
}

get_response = requests.get(endpoint, headers=headers)
print(get_response.json())
