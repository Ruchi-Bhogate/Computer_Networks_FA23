#include <stdio.h>
#include <string.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);



/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];

  /* 
     STUDENT CODE HERE
   */
  
  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
  char response[4096];
  send_smtp(socket, "HELO iu.edu\r\n", response, 4096);
  printf("%s\n", response);
  char msg1[100];
  strcpy(msg1,"MAIL FROM:");
  strcat(msg1,rcpt);
  strcat(msg1,"\r\n");
  send_smtp(socket, msg1, response, 4096);
  printf("%s\n", response);
  char msg2[100];
  strcpy(msg2,"RCPT TO:");
  strcat(msg2,rcpt);
  strcat(msg2,"\r\n");
  send_smtp(socket, msg2, response, 4096);
  printf("%s\n", response);
  send_smtp(socket, "DATA\r\n", response, 4096);
  printf("%s\n", response);
  FILE *fptr;
  fptr = fopen(filepath, "r");
  char s1[100];
  char email[5000];
  while(fgets(s1,100,fptr)){
    strcat(email,s1);
  }
  fclose(fptr);
  strcat(email,"\r\n.\r\n");
  send_smtp(socket, email, response, 4096);
  printf("%s\n", response);

  return 0;
}
