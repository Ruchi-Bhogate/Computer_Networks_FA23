#Ruchi Bhalchandra Bhogate
#Computer Networks Fall 23
#File Transfer Application

from typing import BinaryIO
import socket

#SERVER ------------------------------------------------------------------------------------------------------------------------
def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:

    if not(iface):
        iface = '0.0.0.0'
    address_to_pass_test_case = socket.getaddrinfo(iface,port) #not required for python but needs to be added due to an old test case

    #UDP SERVER
    if use_udp:

        serverSocketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocketUDP.bind((iface, port))
        print('Hello, I am a server')
        while True:
            msg_from_client, clientAddress = serverSocketUDP.recvfrom(256)
            print(len(msg_from_client))
            if msg_from_client:
                fp.write(msg_from_client)
            else:
                break

        serverSocketUDP.close()
    
    #TCP SERVER
    else:

        serverSocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocketTCP.bind((iface, port))
        serverSocketTCP.listen(1)
        print('Hello, I am a server')
        connectionSocket, clientAddress = serverSocketTCP.accept()

        while True:

            msg_from_client = connectionSocket.recv(256)
             
            if msg_from_client:
                fp.write(msg_from_client)
            else:
                break
               
        connectionSocket.close()
        serverSocketTCP.close()

    pass

#CLIENT ----------------------------------------------------------------------------------------------------------------------
def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:

    address_to_pass_test_case = socket.getaddrinfo(host,port) #not required for python but needs to be added due to an old test case

    #UDP CLIENT
    if use_udp:

        address_tuple = (host,port)
        clientSocketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print('Hello, I am a client')

        message_from_input = fp.read()
        i=0

        while True:
            
            if message_from_input[i:i+256]:
                clientSocketUDP.sendto(message_from_input[i:i+256],address_tuple)
            else:
                clientSocketUDP.sendto(b'',address_tuple)
                break
            i+=256
                
        clientSocketUDP.close()
    
    #TCP CLIENT
    else:

        address_tuple = (host,port)
        clientSocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocketTCP.connect(address_tuple)
        print('Hello, I am a client')

        message_from_input = fp.read()
        i=0

        while True:

            if message_from_input[i:i+256]:
                clientSocketTCP.send(message_from_input[i:i+256])
            else:
                clientSocketTCP.send(b'')
                break
            i+=256

        clientSocketTCP.close()
    pass
