import requests

response = requests.get(
    "http://localhost:5000/latest"
)

print("Latest temperature:")
print(response.json())

response = requests.get(
    "http://localhost:5000/temperatures"
)

print("Historical data:")
print(response.json())