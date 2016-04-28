#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFF_SIZE 100

int main(){
	int sock = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP);
	int i=3;
	sockaddr_in serverAddr;
	memset(&serverAddr,0,sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	serverAddr.sin_port = htons(8081);

	bind(sock,(struct sockaddr*)&serverAddr,sizeof(serverAddr));
	
	while(i--){
		sockaddr_in clientAddr;
		socklen_t socklen = sizeof(clientAddr);
		char buffer[BUFF_SIZE];
		/** 注意 最后一个参数,传socklen的地址而不是值 **/
		int len = recvfrom( sock, buffer, BUFF_SIZE,0,(struct sockaddr*)&clientAddr,&socklen); 
		sendto(sock,buffer,len,0,(struct sockaddr*)&clientAddr,sizeof(clientAddr));
	}
	close(sock);
}
