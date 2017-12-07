# cctv processor Info
def getCctvProcessorInfo():
    cctvId = 'cctv_1'

    return {'cctvId':cctvId}

# Socket Server Connect Info
def getSocketInfo():
    host = '127.0.0.1'
    port = 3334
    return {'host': host, 'port': port}

# Web Server Controller Info
def getWebServerInfo():
    host = 'http://127.0.0.1:3333'
    # Get Submit Cctv Status
    cctvStatusManagerUrl = '/cctv_status_receiver'
    # Post Submit Image File
    imageReceiveManagerUrl = '/ay'
    # Receive Command By WebServer (Polling)
    checkCommanderUrl = '/check_commander'
    return {'host': host, 'cctvStatusManagerUrl': cctvStatusManagerUrl, 'imageReceiveManagerUrl': imageReceiveManagerUrl, 'checkCommanderUrl': checkCommanderUrl}
