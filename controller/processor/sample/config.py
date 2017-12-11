
# ultrasound HC-SR04
def getUltrasoundInfo():
    TRIGGER = 18
    ECHO = 24

    return {'TRIGGER':TRIGGER, 'ECHO':ECHO}

# cctv processor Info
def getCctvProcessorInfo():
    cctvId = 'aaaa'

    return {'cctvId':cctvId}

# Socket Server Connect Info
def getSocketInfo():
    host = '192.168.0.3'
    port = 3334
    return {'host': host, 'port': port}

# Web Server Controller Info
def getWebServerInfo():
    host = 'http://192.168.0.3:3333'
    # Get Submit Cctv Status
    cctvStatusManagerUrl = '/cctv_status_receiver'
    # Post Submit Image File
    imageReceiveManagerUrl = '/image_receiver'
    # Receive Command By WebServer (Polling)
    checkCommanderUrl = '/check_commander'
    return {'host': host, 'cctvStatusManagerUrl': cctvStatusManagerUrl, 'imageReceiveManagerUrl': imageReceiveManagerUrl, 'checkCommanderUrl': checkCommanderUrl}
