//Ruchi Bhalchandra Bhogate
//Computer Networks Fall 23
//Assignment 3 DNS Lookup
#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <arpa/inet.h>

int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  long port = atoi(argv[2]);
  char port_char[20];

  sprintf(port_char,"%ld",port);
  struct addrinfo hints;
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_protocol = IPPROTO_TCP;
  hints.ai_flags = AI_PASSIVE;

  struct addrinfo *res,*temp;

  getaddrinfo(host,port_char,&hints,&res);

  temp = res;

  void* raw_addr;

  char buffer[5000];

  while(temp!=NULL){
    
    if (temp->ai_family == AF_INET) { // Address is IPv4
    struct sockaddr_in* tmp = (struct sockaddr_in*)temp->ai_addr;
    raw_addr = &(tmp->sin_addr);
    inet_ntop(AF_INET,raw_addr,buffer,5000);
    printf("IPv4 %s\n",buffer);
    }
    else { // Address is IPv6
    struct sockaddr_in6* tmp = (struct sockaddr_in6*)temp->ai_addr;
    raw_addr = &(tmp->sin6_addr);
    inet_ntop(AF_INET6,raw_addr,buffer,5000);
    printf("IPv6 %s\n",buffer);
    }
    temp = temp->ai_next;
  }

  return 0;
}
