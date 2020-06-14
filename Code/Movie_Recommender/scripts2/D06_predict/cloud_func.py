import requests
url = 'http://predict.dns.internal'
data = '''{Test1: test2}'''
response = requests.post(url, data=data)
print(response.status_code)
print(response.text)
print(response.json())