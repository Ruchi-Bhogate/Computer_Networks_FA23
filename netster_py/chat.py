#Ruchi Bhalchandra Bhogate
#Computer Networks Fall 23
#Socket Programming

import socket
import threading

#SERVER ---------------------------------------------------
def chat_server(iface:str, port:int, use_udp:bool) -> None:
    
    #UDP SERVER
    if use_udp:

        serverSocketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocketUDP.bind((iface, port))
        print('Hello, I am a server')
        
        while True:

            msg_from_client, clientAddress = serverSocketUDP.recvfrom(256)
            msg_from_client = msg_from_client.decode()

            if msg_from_client == 'hello':
                serverSocketUDP.sendto('world'.encode(), clientAddress)
            elif msg_from_client == 'goodbye':
                serverSocketUDP.sendto('farewell'.encode(), clientAddress)
            elif msg_from_client == 'exit':
                serverSocketUDP.sendto('ok'.encode(), clientAddress)
                break
            else:
                serverSocketUDP.sendto(msg_from_client.encode(), clientAddress)

        serverSocketUDP.close()
    
    #TCP SERVER
    else:

        serverSocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocketTCP.bind((iface, port))
        serverSocketTCP.listen(1)
        print('Hello, I am a server')

        connection_counter = -1

        while True:

            connectionSocket, clientAddress = serverSocketTCP.accept()
            connection_counter += 1
            print('connection ', connection_counter, ' from ', clientAddress)
            new_thread = threading.Thread(target = tcp_connection, args = (connectionSocket, clientAddress, serverSocketTCP))
            new_thread.start()

    pass

#CLIENT --------------------------------------------------
def chat_client(host:str, port:int, use_udp:bool) -> None:
    
    #UDP CLIENT
    if use_udp:

        address_tuple = (host,port)
        clientSocketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print('Hello, I am a client')

        while True:

            message_from_input = input()
            clientSocketUDP.sendto(message_from_input.encode(),address_tuple)
            msg_from_server, address = clientSocketUDP.recvfrom(256)
            msg_from_server = msg_from_server.decode()

            print(msg_from_server)

            if (message_from_input == 'goodbye' and msg_from_server == 'farewell') or (message_from_input == 'exit' and msg_from_server == 'ok'):
                break

        clientSocketUDP.close()
    
    #TCP CLIENT
    else:

        address_tuple = (host,port)
        clientSocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocketTCP.connect(address_tuple)
        print('Hello, I am a client')

        while True:

            message_from_input = input()
            clientSocketTCP.send(message_from_input.encode())
            msg_from_server = clientSocketTCP.recv(256)
            msg_from_server = msg_from_server.decode()

            print(msg_from_server)

            if (message_from_input == 'goodbye' and msg_from_server == 'farewell') or (message_from_input == 'exit' and msg_from_server == 'ok'):
                break

        clientSocketTCP.close()

    pass

def tcp_connection(connectionSocket,clientAddress,serverSocketTCP):

    while True:

        msg_from_client = connectionSocket.recv(256)
        print('got message from ', clientAddress)
        msg_from_client = msg_from_client.decode()
        
        if msg_from_client == 'hello':
            connectionSocket.send('world'.encode())
        elif msg_from_client == 'goodbye':
            connectionSocket.send('farewell'.encode())
            connectionSocket.close()
            break
        elif msg_from_client == 'exit':
            connectionSocket.send('ok'.encode())
            connectionSocket.close()
            serverSocketTCP.close()
            break
        else:
            connectionSocket.send(msg_from_client.encode())
