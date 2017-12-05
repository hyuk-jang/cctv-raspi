import os
import urllib3
import json


def requestGetHttp(httpPath):
    try:
        http = urllib3.PoolManager(retries=False)
        r = http.request('GET', httpPath)
        return True if r.status == 200 else False
        # resJson = json.loads(r.data.decode('utf-8'))
        # return resJson
    except (urllib3.exceptions.NewConnectionError) as e:
        print(e)
        return False
    except e:
        print('default Error')
        return False


def requestPostHttp(httpPath, fileName, ext):
    print(httpPath, fileName)
    try:
        filePath = os.getcwd() + '/sample/image/' + fileName + '.' + ext
        print('filePath\t',filePath) 
        with open(filePath, 'rb') as img:
            binary_data = img.read()

        http = urllib3.PoolManager(retries=False)
        r = http.request(
            'POST',
            httpPath + ':' + fileName,
            body = binary_data,
            headers={'Content-Type': 'image/jpeg'})
        return True if r.status == 200 else False
    except UnicodeDecodeError as e:
        print(e)
        return False
    except (urllib3.exceptions.NewConnectionError) as e:
        print(e)
        return False
    except :
        print('default Error')
        return False


# def submitImgWithSocket(socketPath, fileName):
