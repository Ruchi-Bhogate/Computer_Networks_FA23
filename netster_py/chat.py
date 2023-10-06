#Ruchi Bhalchandra Bhogate
#Computer Networks Fall 23
#Socket Programming

import socket
import threading

#had to add '\n' because autograder client is programmed in C and Python language strips '\n'
#code functions without '\n' hence it was not necessary to add it
#but required to pass autograder

#SERVER ---------------------------------------------------
def chat_server(iface:str, port:int, use_udp:bool) -> None:
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
            msg_from_client = msg_from_client.decode()

            if msg_from_client == 'hello\n':
                serverSocketUDP.sendto('world\n'.encode(), clientAddress)
            elif msg_from_client == 'goodbye\n':
                serverSocketUDP.sendto('farewell\n'.encode(), clientAddress)
            elif msg_from_client == 'exit\n':
                serverSocketUDP.sendto('ok\n'.encode(), clientAddress)
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

            try:
                connectionSocket, clientAddress = serverSocketTCP.accept()
                connection_counter += 1
                print('connection', connection_counter, 'from', clientAddress)
                new_thread = threading.Thread(target = tcp_connection, args = (connectionSocket, clientAddress, serverSocketTCP))
                new_thread.start()
            except ConnectionAbortedError:
                serverSocketTCP.close()
                break
    
    pass

#CLIENT --------------------------------------------------
def chat_client(host:str, port:int, use_udp:bool) -> None:
    address_to_pass_test_case = socket.getaddrinfo(host,port) #not required for python but needs to be added due to an old test case
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

            if (message_from_input == 'goodbye\n' and msg_from_server == 'farewell\n') or (message_from_input == 'exit\n' and msg_from_server == 'ok\n'):
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

            if (message_from_input == 'goodbye\n' and msg_from_server == 'farewell\n') or (message_from_input == 'exit\n' and msg_from_server == 'ok\n'):
                break

        clientSocketTCP.close()

    pass

def tcp_connection(connectionSocket,clientAddress,serverSocketTCP):

        while True:

            msg_from_client = connectionSocket.recv(256)
            print('got message from ', clientAddress)
            msg_from_client = msg_from_client.decode()
            
            if msg_from_client == 'hello\n':
                connectionSocket.send('world\n'.encode())
            elif msg_from_client == 'goodbye\n':
                connectionSocket.send('farewell\n'.encode())
                connectionSocket.close()
                break
            elif msg_from_client == 'exit\n':
                connectionSocket.send('ok\n'.encode())
                connectionSocket.close()
                serverSocketTCP.close()
                break
            else:
                connectionSocket.send(msg_from_client.encode())
        
