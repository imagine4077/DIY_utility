#include <arpa/inet.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#define BUFFER_SIZE 1024

int main(){
	int sock_server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	sockaddr_in server_addr;
	memset(&server_addr,0,sizeof(server_addr));
	server_addr.sin_port = htons(1234);
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	server_addr.sin_family = AF_INET;

	bind(sock_server, (struct sockaddr*)&server_addr, sizeof(server_addr));
	listen(sock_server,20);
//	while(1){
		sockaddr_in client_addr;
		socklen_t caddr_len = sizeof(client_addr);
		int sock_client = accept(sock_server,(struct sockaddr*)&client_addr,&caddr_len);
		int count;
		char buffer[BUFFER_SIZE];
		int fl = read(sock_client,buffer,BUFFER_SIZE); // 注意此处 从 sock_client 读取数据,sock_server 只负责监听请求,sock_client负责收发数据
		printf("the file client want:%s\n",buffer);
		FILE* fp = fopen(buffer,"r");
		if(!fp){
			char err_msg[] = "open file failed\n";
			write(sock_client,err_msg,strlen(err_msg)+1);
			write(sock_client,buffer,fl+3);
			close(sock_client);
			close(sock_server);
			exit(1);
		}
		float sum_xmited=0.0;
		printf("0 MB tx\n");
		while((count=fread(buffer,1,BUFFER_SIZE,fp))>0){
			write(sock_client,buffer,count);
			sum_xmited += count/(1024*1024.0);
			if(((int)sum_xmited)%10==0){
				printf("\033[1A"); //回到上一行
				printf("\033[K"); //删除该行
				printf("%f MB tx\n",sum_xmited);
			}
		}
		printf("tx success\n");
//	}
	fclose(fp);
	close(sock_client);
	close(sock_server);
}
