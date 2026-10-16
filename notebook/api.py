'''import requests

response=requests.get("https://httpbin.org/get")

print(response.status_code)

data=response.json()

print(data.keys())
print(type(data))
print(data["origin"])'''


import requests

def get_api_data():
    response=requests.get("https://httpbin.org/get")
    data=response.json()
    
    return data

data =get_api_data()
print(data["url"])