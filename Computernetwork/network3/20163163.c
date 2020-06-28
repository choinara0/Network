/*
Student ID : 20163163
Name : Choinara
*/


#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFSIZE 100
void error_handling(char *message);
void display();
#define MAXCLIENT (8)
int clienttcpSocket[MAXCLIENT];

int main(int argc, char **argv) {

  int tcpServ_sock;

  struct sockaddr_in tcpServer_addr;
  struct sockaddr_in tcpClient_addr;
  struct sockaddr_in newTcp_addr;


  for(int i = 0; i < MAXCLIENT; i++) {
  	clienttcpSocket[i] = -1;;
  }

  int slot;
  socklen_t client_length;

  fd_set reads, temps;
  int fd_max;


  char str[BUFSIZE];
  int option = 2;

  char *tcpport = NULL;

  if(argc != 2) {
    printf("Usage : %s <tcpport> \n", argv[0]);
    exit(1);
  }

  tcpport = argv[1];

  display();

  tcpServ_sock = socket(PF_INET, SOCK_STREAM, 0);
  if(tcpServ_sock == -1)
	  error_handling("socket() error");

  memset(&tcpServer_addr, 0 , sizeof(tcpServer_addr));
  tcpServer_addr.sin_family = AF_INET;
  tcpServer_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  tcpServer_addr.sin_port = htons(atoi(tcpport));

  setsockopt(tcpServ_sock, SOL_SOCKET, SO_REUSEADDR, (const void *)&option, sizeof(int));
  if(bind(tcpServ_sock, (struct sockaddr *) &tcpServer_addr, sizeof(tcpServer_addr)) == -1 )
	  error_handling("bind() error");


  if(listen(tcpServ_sock, 5)==-1)
    error_handling("listen() error");

  FD_ZERO(&reads);
  FD_SET(tcpServ_sock, &reads);
  fd_max = tcpServ_sock;


  while(1) {
    int nfound = 0;

    temps = reads;

    nfound = select(fd_max+1, &temps, 0, 0, NULL);

	  if(FD_ISSET(tcpServ_sock, &temps)) {

		  FD_CLR(tcpServ_sock, &temps);
	    // NEED TO IMPLEMENT HERE
      int index_num = -1;
      client_length = sizeof(tcpClient_addr);

      while(clienttcpSocket[++index_num] != -1) {

        if(index_num ==16) {
          break;
        }

      }

      if(index_num==16) {
        unsigned int ctemp = accept(tcpServ_sock, (struct sockaddr *)&tcpClient_addr, &client_length);
        break;
      }

      else {
        clienttcpSocket[index_num] = accept(tcpServ_sock, (struct sockaddr *)&tcpClient_addr, &client_length);
        if (clienttcpSocket[index_num] < 0) {
			    continue;
		    }

        FD_SET(clienttcpSocket[index_num], &reads);
	      fd_max = clienttcpSocket[index_num];
		    printf("connection from host %s, port %d, socket %d\n", inet_ntoa(tcpClient_addr.sin_addr), ntohs(tcpClient_addr.sin_port),clienttcpSocket[index_num]);

      }
	  }

    else {
		  for(int i = 0; i < MAXCLIENT; i++) {
		    if (FD_ISSET(clienttcpSocket[i], &temps)) {
			    FD_CLR(clienttcpSocket[i], &temps);


         memset(str, 0, sizeof(str));
         unsigned int bytesread = read(clienttcpSocket[i], str, BUFSIZE);

          if(bytesread <= 0) {
            printf("Connection closed %d\n", clienttcpSocket[i]);
            clienttcpSocket[i] = -1;
          }

			    // NEED TO IMPLEMENT HERE
          for(int j = 0; j < MAXCLIENT; j++) {
            if(j == i || clienttcpSocket[j] == -1) {
              continue;
            }

            write(clienttcpSocket[j], str, bytesread);

          }

        }

		  }

	  }

  }//while End
}//main End

void display() {
	printf("Student ID : 20163163 \n");
	printf("Name : Nara Choi  \n");
}

void error_handling(char *message) {
  fputs(message, stderr);
  fputc('\n', stderr);
  perror("hw4 error");
  exit(1);
}
