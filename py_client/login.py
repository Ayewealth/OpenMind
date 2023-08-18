import requests

endpoint = "http://127.0.0.1:8000/token/"
# headers = {
#     "Authorization": "Token 29c0674048f480f86a295424b364027ba5b30bcb"
# }
data = {
    "email": "emi@gmail.com",
    "password": "emi15082005"
}
get_response = requests.post(endpoint, json=data)
print(get_response.json())
