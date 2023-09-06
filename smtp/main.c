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

  char response[4096];
  //Starting the connection to the SMTP server
  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
  //Sending message to the server and getting back the response
  send_smtp(socket, "HELO iu.edu\r\n", response, 4096);
  //Printing the response of the server
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

  //Reading the txt file that contains email data
  FILE *f;
  f = fopen(filepath, "r");
  char s[100];
  char email[4096];

  //To clear the character array before storing the file content
  for(int i=0; i<4096; i++){
    email[i] = '\0';
  }

  while(fgets(s,100,f)){
    strcat(email,s);
  }
  fclose(f);
  //Adding trailing period to complete the exchange
  strcat(email,"\r\n.\r\n");

  send_smtp(socket, email, response, 4096);
  printf("%s\n", response);

  return 0;
}
