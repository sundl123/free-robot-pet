/*************************************************
* @par Copyright (C): 2010-2019, hunan CLB Tech
* @file         car_server.c
* @version      V2.0
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

#include <wiringPi.h>
#include <softPwm.h>

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

/*******************舵机定义*************************
*****************************************************/
int myservo1 = 15; //舵机0 手爪
int myservo2 = 14; //舵机1 上臂
int myservo3 = 13; //舵机2 下臂
int myservo4 = 12; //舵机3 底座

int yunservo1 = 10; //左右云台
int yunservo2 = 9; //上下云台

//int SERVOS = 4;   //说明有4个舵机
float currentAngle[4];
float s_MIN[4];
float s_MAX[4];
float INITANGLE[4];

int lr_detection = 90;   //摄像头云台舵机左右
int qh_detection = 90;    //摄像头云台舵机上下
int flag = 0;            //标志位

#define ServoDelayTime 50
int delta = 5;  //舵机转动幅度
int delta_bottom = 2; //底座舵机转动幅度
/*******************舵机函数定义*************************
*********************************************************/
void ClampOpen()                //手爪打开
{
  set_servo_angle(myservo1,s_MAX[3]); 
  delay(300);
}
void ClampClose()
{
    set_servo_angle(myservo1,s_MIN[3]);   //手爪闭合
    delay(300);
}
void BottomLeft()             // 底座左转
{
  if(currentAngle[0] + delta_bottom < s_MAX[0]) 
    {currentAngle[0] += delta_bottom;}
    set_servo_angle(myservo4,currentAngle[0]);
}
void BottomRight()             // 底座右转
{
  if(currentAngle[0] - delta_bottom > s_MIN[0]) 
  {currentAngle[0] -= delta_bottom;}
    set_servo_angle(myservo4,currentAngle[0]);
}

void Arm_A_Up()            //上臂舵机向上
{
  if(currentAngle[2] + delta < s_MAX[2])
    currentAngle[2] += delta;
   set_servo_angle(myservo2,currentAngle[2]);
}

void Arm_A_Down()      //上臂舵机向下
{
  if(currentAngle[2] - delta > s_MIN[2])
    currentAngle[2] -= delta;
   set_servo_angle(myservo2,currentAngle[2]);
}

void Arm_B_Up()     //下臂舵机上升
{
  if(currentAngle[1] - delta >  s_MIN[1])
    currentAngle[1] -= delta;
   set_servo_angle(myservo3,currentAngle[1]);
}

void Arm_B_Down()  //下臂舵机下降
{
  if(currentAngle[1] + delta < s_MAX[1])
    currentAngle[1] += delta;
   set_servo_angle(myservo3,currentAngle[1]);
}

void Servo_stop() //停止所有舵机
{
  set_servo_angle(myservo1,currentAngle[3]);
  set_servo_angle(myservo2,currentAngle[2]);
  set_servo_angle(myservo3,currentAngle[1]);
  set_servo_angle(myservo4,currentAngle[0]);
}

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
    
    //手爪舵机
    s_MIN[3] = 15;
    s_MAX[3] = 95;
    INITANGLE[3] = 28;
    
    //上臂舵机
    s_MIN[2] = 10;
    s_MAX[2] = 140;
    INITANGLE[2] = 90;
    
    //下臂舵机
    s_MIN[1] = 40;
    s_MAX[1] = 170;
    INITANGLE[1] = 90;
    
    //底座舵机
    s_MIN[0] = 0;
    s_MAX[0] = 170;
    INITANGLE[0] = 90;
    
    //初始化舵机    
    set_servo_angle(myservo1,INITANGLE[3]); //手爪舵机
    set_servo_angle(myservo2,INITANGLE[2]); //上臂舵机
    set_servo_angle(myservo3,INITANGLE[1]); //下臂舵机
    set_servo_angle(myservo4,INITANGLE[0]); //底座舵机
	
    set_servo_angle(yunservo1,lr_detection); //云台左右控制
    set_servo_angle(yunservo2,qh_detection); //云台上下控制
    
    currentAngle[3] = INITANGLE[3];
    currentAngle[2] = INITANGLE[2];
    currentAngle[1] = INITANGLE[1];
    currentAngle[0] = INITANGLE[0];  
    
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
					case 'A':t_up(80,0);      printf("forward\n");break;
					case 'B':t_down(80,0);    printf("back\n");break;            						
					case 'C':moveLeft(80,0);    printf("left\n");break;
					case 'D':moveRight(80,0);   printf("right\n");break;
					case 'E':t_stop(0);       printf("stop\n");break;
					case '1':printf("Arm A Up\n");Arm_A_Up();delay(ServoDelayTime);break;//上臂上升
					case '2':if(flag == 0){printf("Clamp Open\n");ClampOpen();flag=1;}else{printf("Clamp  Close\n");ClampClose();flag=0;}break;//手爪控制
					case '3':printf("Arm B Up\n");Arm_B_Up();delay(ServoDelayTime);break;//下臂上升
					case '4':printf("Arm A down\n");Arm_A_Down();delay(ServoDelayTime);break;//上臂下降
					case '6':printf("Arm B down\n");Arm_B_Down();delay(ServoDelayTime);break;//下臂下降
		                        case 'I':lr_detection += 10;if(lr_detection <= 0) lr_detection = 0; if(lr_detection>=180) lr_detection = 180; set_servo_angle(yunservo1,lr_detection);  break;//左
					case 'L':lr_detection -= 10;if(lr_detection <= 0) lr_detection = 0; if(lr_detection>=180) lr_detection = 180; set_servo_angle(yunservo1,lr_detection);  break;//右
					case 'K':qh_detection += 10;if(qh_detection <= 0) qh_detection = 0; if(qh_detection>=180) qh_detection = 180; set_servo_angle(yunservo2,qh_detection);  break;//上
					case 'J':qh_detection -= 10;if(qh_detection <= 0) qh_detection = 0; if(qh_detection>=180) qh_detection = 180; set_servo_angle(yunservo2,qh_detection);  break;//下
					case 'G':printf("MeArm turn Left\n");BottomLeft();delay(ServoDelayTime);break;//底部舵机左转
					case 'H':printf("MeArm turn Right\n");BottomRight();delay(ServoDelayTime);break;//底部舵机右转
					default: t_stop(0); printf("stop\n");break;
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

