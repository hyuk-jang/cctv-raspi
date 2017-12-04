
import urllib3
import json

http = urllib3.PoolManager()

r = http.request('GET', 'http://localhost:3333')

resJson = json.loads(r.data.decode('utf-8'))

print(resJson)
