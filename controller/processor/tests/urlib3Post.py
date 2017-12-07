# Image를 Http Post 방식으로 보내고자 할 경우 (이번 CCTV 프로젝트에서는 쓰지 않음)
# FIXME 아직 완성되지 않음 (테스트해보지 못함)
def requestPostHttp(httpPath, fileName):
    print('requestPostHttp', httpPath, fileName)
    # TEST 파일명 고정으로 해봄
    fileName = 'aaaa'
    filePath = os.getcwd() + '/sample/image/' + fileName + '.png'
    try:
        filePath = os.getcwd() + '/sample/image/' + fileName + '.png'
        print('filePath\t', filePath)
        with open(filePath, 'rb') as img:
            binary_data = img.read()

        print('binary_data',binary_data)
        http = urllib3.PoolManager(retries=False)
        r = http.request(
            'POST',
            httpPath + ':' + fileName,
            body = binary_data,
            headers = {'Content-Type': 'image/jpeg'})
        return True if r.status == 200 else False
    except UnicodeDecodeError as e:
        print(e)
        return False
    except (urllib3.exceptions.NewConnectionError) as e:
        print(e)
        return False
    except:
        print('default Error')
        return False