#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>

#define BUFFER_SIZE 1024

int main(int argc, char* argv[]){
	printf("server addr:%s\ntarget file:%s\n",argv[1],argv[2]);
	int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

	sockaddr_in server_addr;
	server_addr.sin_port = htons(1234);
	server_addr.sin_addr.s_addr = inet_addr(argv[1]);
	server_addr.sin_family = AF_INET;

	FILE* fp = fopen(argv[2],"wb");
	if(!fp){
		printf("create newfile failed\n");
		exit(1);
	}

	connect(sock,(struct sockaddr*)&server_addr,sizeof(server_addr));
	int count;
	char buffer[BUFFER_SIZE];
	float sum_xmited=0.0;
	strcpy(buffer,argv[2]);
	write(sock,buffer,strlen(buffer)+3);
	printf("0 MB txed\n");
	while((count=read(sock,buffer,BUFFER_SIZE))>0){
		fwrite(buffer,count,1,fp);
		sum_xmited += count/(1024*1024.0);
			if(((int)sum_xmited)%10==0){
				printf("\033[1A"); //回到上一行
				printf("\033[K"); //删除该行
				printf("%f MB tx\n",sum_xmited);
			}
	}
	printf("tx success\n");
	fclose(fp);
	close(sock);
}
