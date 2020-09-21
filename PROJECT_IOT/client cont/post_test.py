import requests
myobj = {
  "id": "string",
  "description": "string",
  "services": [
    {
      "id": "eyasssssssssss",
      "type": "string",
      "title": "string",
      "description": "string",
      "meta": {},
      "apis": [
        {
          "id": "string",
          "title": "string",
          "description": "string",
          "protocol": "string",
          "url": "string",
          "spec": {
            "mediaType": "string",
            "url": "string",
            "schema": {}
          },
          "meta": {}
        }
      ],
      "doc": "string",
      "ttl": 0,
      "createdAt": "2020-05-25T22:42:41.630Z",
      "updatedAt": "2020-05-25T22:42:41.630Z",
      "expiresAt": "2020-05-25T22:42:41.630Z"
    }
  ],
  "page": 0,
  "per_page": 0,
  "total": 0
}

# url = 'http://localhost:8082'

# # print(requests.get(url).text)
# x = requests.post(url, data = myobj)
# print(x)
# print(x.text)
# print(myobj)

url = 'http://localhost:8082'
# url = 'http://127.0.0.1:8082'
x = requests.get('http://www.google.com')
# x = requests.post(url, data = myobj)
print(x)