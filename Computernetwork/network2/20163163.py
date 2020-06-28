from socket import *
import os
import sys

print("Student ID : 20163163")
print("Name : Nara Choi")

portnumber = int(sys.argv[1])

serversocket = socket(AF_INET, SOCK_STREAM)

serversocket.bind(('',portnumber))

serversocket.listen(3)

while(1):

    clientsocket, addressFamiliy = serversocket.accept()

    print("Connection : Host IP %s, Port %s, socket %d" %(addressFamiliy[0],addressFamiliy[1],clientsocket.fileno()))
    request = clientsocket.recv(1024).decode().split('\r\n')
    for i in range(len(request)-1):
        print(request[i])

    filename = request[0].split(' /')[1].split(' ')[0]

    try:
        f = open(filename, 'rb')
        data = f.read()
        filesize = os.path.getsize(filename)
        temp = 'HTTP/1.0 200 OK\r\n' \
                             'Connection: close\r\n' \
                             'ID: 20163163\r\n' \
                             'Name: Nara Choi\r\n' \
                             'Content-Length: %s\r\n' \
               'Content-Type: text/html\r\n\r\n%s'%(str(filesize),data.decode())

        clientsocket.sendall(temp.encode())

    except FileNotFoundError:
        print("Server Error : No such file ./%s!" %(filename))
        #print("Connection : Host IP %s, Port %s, socket %d" % (addressFamiliy[0], addressFamiliy[1], clientsocket.fileno()))
        temp = 'HTTP/1.0 404 NOT FOUND\r\n' \
                'Connection: close\r\n' \
                'ID: 20163163 \r\n' \
                'Name: Nara Choi\r\n' \
                'Content-Length: 0\r\n' \
                'Content-Type: text/html\r\n\r\n'

        clientsocket.sendall(temp.encode())

        continue
    clientsocket.close()