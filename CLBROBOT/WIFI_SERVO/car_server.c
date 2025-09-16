/*************************************************
* @par Copyright (C): 2010-2019, hunan CLB Tech
* @file         car_server.c
* @version      V1.0
* @details
* @par History

@author: zhulin
***************************************************/
#include "LOBOROBOT.h"
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <time.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define BUFSIZE 512

void  Handler(int signo)
{
    //System Exit
    printf("\r\nHandler:Motor Stop\r\n");
    Motor_Stop(MOTORA);
    Motor_Stop(MOTORB);
    Motor_Stop(MOTORC);
    Motor_Stop(MOTORD);
    DEV_ModuleExit();

    exit(0);
}


float lr_detection = 90;
float qh_detection = 90;



typedef struct CLIENT {
	int fd;
	struct sockaddr_in addr;
}CLIENT;

int main(int argc, char *argv[])
{
    int sockfd;
    int listenfd;
    int connectfd;

    int ret;
    int maxfd=-1;
    struct timeval tv;

    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;

    socklen_t len;
    int portnumber;

    char buf[BUFSIZE];

    int z,i,maxi = -1;
    fd_set rset,allset;

    CLIENT client[FD_SETSIZE];
       // 电机初始化
    Motor_Init();

    set_servo_angle(10,lr_detection);
    set_servo_angle(9,qh_detection); //初始化云台
	/********PWM 控制*********************/
    if(argc != 2)
    {
        printf("Please add portnumber!");
        exit(1);
    }

    if((portnumber = atoi(argv[1]))<0)
    {
        printf("Enter Error!");
        exit(1);
    }


    if((listenfd = socket(PF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("Socket Error!");
        exit(1);
    }


    memset(&server_addr, 0, sizeof server_addr);
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(portnumber);


    if((bind(listenfd, (struct sockaddr *)(&server_addr), sizeof server_addr)) == -1)
    {
        printf("Bind Error!");
        exit(1);
    }

    if(listen(listenfd, 128) == -1)
    {
        printf("Listen Error!");
        exit(1);
    }

    for(i=0;i<FD_SETSIZE;i++)
    {
	client[i].fd = -1;
    }

    FD_ZERO(&allset);
    FD_SET(listenfd, &allset);

    maxfd = listenfd;

    printf("waiting for the client's request...\n");
    
        // Exception handling:ctrl + c
    signal(SIGINT, Handler);

    while (1)
    {
	rset = allset;

	tv.tv_sec = 0;      //wait 1u second
        tv.tv_usec = 1;
    
        ret = select(maxfd + 1, &rset, NULL, NULL, &tv);
    
	if(ret == 0)
	    continue;
	else if(ret < 0)
	{
	    printf("select failed!");
       	    break;
	}
	else
	{
	    if(FD_ISSET(listenfd,&rset)) // new connection
	    {
		len = sizeof (struct sockaddr_in);
		if((connectfd = accept(listenfd,(struct sockaddr*)(&client_addr),&len)) == -1)
		{
		    printf("accept() error");
		    continue;
                }

		for(i=0;i<FD_SETSIZE;i++)
		{
		    if(client[i].fd < 0)
		    {
		        client[i].fd = connectfd;
			client[i].addr = client_addr;
			printf("Yout got a connection from %s\n",inet_ntoa(client[i].addr.sin_addr));
			break;
		    }
		}

		if(i == FD_SETSIZE)
		    printf("Overfly connections");

		FD_SET(connectfd,&allset);

		if(connectfd > maxfd)
		    maxfd = connectfd;

		if(i > maxi)
		    maxi = i;
	    }
	    else
	    {
		for(i=0;i<=maxi;i++)
		{
		    if((sockfd = client[i].fd)<0)
		        continue;

                    if(FD_ISSET(sockfd,&rset))
		    {
			bzero(buf,BUFSIZE + 1);
			if((z = read(sockfd,buf,sizeof buf)) >0)
			{
      		  buf[z] = '\0';
            printf("num = %d received data:%s\n",z,buf);
			  if(z == 3 || z == 6)
			    {
				if(buf[0] == 'O' && buf[1] == 'N')
				{
	     		switch(buf[2])
		         	{
					case 'A':t_up(50,0);      printf("forward\n");break;
					case 'B':t_down(50,0);    printf("back\n");break;            						
					case 'C':moveLeft(50,0);    printf("left\n");break;
					case 'D':moveRight(50,0);   printf("right\n");break;
					case 'E':t_stop(0);       printf("stop\n");break;
					case 'I':lr_detection += 10;if(lr_detection <= 0) lr_detection = 0; if(lr_detection>=180) lr_detection = 180; set_servo_angle(10,lr_detection);  break;//左
					case 'L':lr_detection -= 10;if(lr_detection <= 0) lr_detection = 0; if(lr_detection>=180) lr_detection = 180; set_servo_angle(10,lr_detection);  break;//右
					case 'K':qh_detection += 10;if(qh_detection <= 0) qh_detection = 0; if(qh_detection>=180) qh_detection = 180; set_servo_angle(9,qh_detection);  break;//上
					case 'J':qh_detection -= 10;if(qh_detection <= 0) qh_detection = 0; if(qh_detection>=180) qh_detection = 180; set_servo_angle(9,qh_detection);  break;//下
					default: t_stop(0);       printf("stop\n");break;
				    }
				}
				else
				{
	
				    t_stop(0);
				}
			    }
			    else if(z == 6)
			    {
				if(buf[2] == 0x00)
				{
				    switch(buf[3])
				    {
					case 0x01:t_up(50,0); printf("forward\n");break;
					case 0x02:t_down(50,0);    printf("back\n");break;							
					case 0x03:moveLeft(50,0);    printf("left\n");break;
					case 0x04:moveRight(50,0);   printf("right\n");break;
					case 0x00:t_stop(0);    printf("stop\n");break;
					default: break;
				    }
				}
				else
				{
				    t_stop(0);
				}
			    }
			    else
			    {
					t_stop(0);
			    }
				
                        }
		        else
		        {
		            printf("disconnected by client!");
	                    close(sockfd);
	                    FD_CLR(sockfd,&allset);
	                    client[i].fd = -1;
		        }
	            }
	        }
            }
        }
    }
    close(listenfd);
    return 0;
}

