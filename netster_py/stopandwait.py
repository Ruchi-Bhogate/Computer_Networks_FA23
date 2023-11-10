#Ruchi Bhalchandra Bhogate
#Computer Networks Fall 23
#RUDP - Stop and Wait

#Questions to ask during Code Review ---------------

# Do I need to seperately write rdt_send and rdt_recv?? Is it okay to write logic inside server and client only?
# msg is 256 data and 2 bytes of ack and sq no, is this okay or should I make it to 254 data so that total packet size is 256?
#It works on autograder

from typing import BinaryIO
import socket

#Since bytes() takes iterable of int
sending_sequence_number = [0]
receiving_sequence_number = [0]
ACK = [1]
NACK = [0]

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:

    global receiving_sequence_number

    if not(iface):
        iface = '0.0.0.0'
    address_to_pass_test_case = socket.getaddrinfo(iface,port) #not required for python but needs to be added due to an old test case

    serverSocketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocketUDP.bind((iface, port))
    print('Hello, I am a server')

    while True:

        msg_from_client, clientAddress = serverSocketUDP.recvfrom(258)

        if msg_from_client:
            #print("srv",len(msg_from_client),msg_from_client[0],msg_from_client[1])
            if msg_from_client[1] == NACK[0]:
                if msg_from_client[0] == receiving_sequence_number[0]:
                    message = bytes(receiving_sequence_number)+bytes(ACK)
                    serverSocketUDP.sendto(message,clientAddress)
                    fp.write(msg_from_client[2:])
                    if msg_from_client[0] == 0:
                        receiving_sequence_number = [1]
                    else:
                        receiving_sequence_number = [0]
                else:
                    message = bytes([msg_from_client[0]])+bytes(ACK)
                    serverSocketUDP.sendto(message,clientAddress)
            else:
                continue
        else:
            break

    serverSocketUDP.close()
    pass

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:

    global sending_sequence_number

    address_to_pass_test_case = socket.getaddrinfo(host,port) #not required for python but needs to be added due to an old test case

    address_tuple = (host,port)
    clientSocketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print('Hello, I am a client')

    message_from_input = fp.read()
    i=0

    while True:
            
        if message_from_input[i:i+256]:
            message = bytes(sending_sequence_number)+bytes(NACK)+message_from_input[i:i+256]
            #print(len(message))
            clientSocketUDP.sendto(message,address_tuple)
            clientSocketUDP.settimeout(0.06)

            try:
                msg_from_server, clientAddress = clientSocketUDP.recvfrom(258)
                #print("ms",msg_from_server)
            except socket.timeout:
                continue

            #print("c",msg_from_server[0],msg_from_server[1])

            if msg_from_server[1] == ACK[0]:
                if msg_from_server[0] == sending_sequence_number[0]:
                    if msg_from_server[0] == 0:
                        sending_sequence_number = [1]
                    else:
                        sending_sequence_number = [0]
            else:
                continue

        else:
            clientSocketUDP.sendto(b'',address_tuple)
            break

        i+=256
                
    clientSocketUDP.close()
    pass
