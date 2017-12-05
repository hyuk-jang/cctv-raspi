import socket                   # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60000                    # Reserve a port for your service.

# connection to hostname on the port.
s.connect((host, port))
s.send("Hello server!")

with open('received_file', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        # Receive no more than 1024 bytes
        data = s.recv(1024)
        print('data=', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')