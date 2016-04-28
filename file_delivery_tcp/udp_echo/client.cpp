#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <iostream>

int main(){
	int sock = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP);
	
	sockaddr_in serverAddr;
	socklen_t addrLen = sizeof(serverAddr);
	memset(&serverAddr,0,sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(8081);
	serverAddr.sin_addr.s_addr = inet_addr("114.212.83.45");

	bind(sock,(struct sockaddr*)&serverAddr,addrLen);

	int i=100;
	while(i--){
		char buffer[100]="Hello albert";
		char ti[8];
		snprintf(ti,8,"%d",i);
		strcat(buffer,ti);
		sendto(sock,buffer,100,0,(struct sockaddr*)&serverAddr,addrLen);
		recvfrom(sock,buffer,100,0,(struct sockaddr*)&serverAddr,&addrLen);
		printf("%s\n",buffer);
	}
	close(sock);
}
