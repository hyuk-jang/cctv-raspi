
import os
import requests
import urllib3


url = 'http://127.0.0.1:3333/up'
fileName = 'aaaa'
filePath = os.getcwd() + '/tests/aaaa.png'

# files = {'file': open(filePath, 'rb')}
# r = requests.post(url, files = files)

# try:
filePath = os.getcwd() + '/image/' + fileName + '.png'
print('filePath\t', filePath)

with open(filePath, 'rb') as img:
    # binary_data = img.read()
    print('파일 읽기 시작')
    byteList = b''
    while True:
        line = img.readline()
        if not line:
            break
        else:
            byteList += line
    print('byteList', byteList.__len__())

print("[+] Sending file...")
print('encoded_image',byteList.__len__())
http = urllib3.PoolManager(retries=False)
r = http.request(
    'POST',
    url + ':' + fileName,
    body = byteList,
    headers = {'Content-Type': 'image/jpeg; encoding:UTF-8'})

print('final result', r)

