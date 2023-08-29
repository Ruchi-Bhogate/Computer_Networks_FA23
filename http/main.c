#include <stdio.h>
#include <string.h>
// Test
void send_http(char* host, char* msg, char* resp, size_t len);


/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
  if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];

  /*
    STUDENT CODE HERE
   */
   char response[5000];
   char msg[1200];
   char s1[50] = " HTTP/1.1\r\n";
   char s2[100] = "Host: ";
   strcpy(msg,verb);
   strcat(path,s1);
   strcat(msg, " ");
   strcat(msg,path);
   strcat(s2,host);
   strcat(msg,s2);
   strcat(msg,"\r\n\r\n");

   send_http(host, msg, response, 5000);
   printf("%s\n", response);
  
  return 0;
}
