#ifndef __LOBOROBOT_H_
#define __LOBOROBOT_H_

#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdint.h>

#define USE_DEBUG 0
#if USE_DEBUG
#define DEBUG(__info,...) printf("Debug : " __info,##__VA_ARGS__)
#else
#define DEBUG(__info,...)
#endif

int fd;
#define UBYTE   uint8_t
#define UWORD   uint16_t
#define UDOUBLE uint32_t

//-------PCA9685 模块--------
#define SUBADR1             0x02
#define SUBADR2             0x03
#define SUBADR3             0x04
#define MODE1               0x00
#define PRESCALE            0xFE
#define LED0_ON_L           0x06
#define LED0_ON_H           0x07
#define LED0_OFF_L          0x08
#define LED0_OFF_H          0x09
#define ALLLED_ON_L         0xFA
#define ALLLED_ON_H         0xFB
#define ALLLED_OFF_L        0xFC
#define ALLLED_OFF_H        0xFD

#define PCA_CHANNEL_0       0
#define PCA_CHANNEL_1       1
#define PCA_CHANNEL_2       2
#define PCA_CHANNEL_3       3
#define PCA_CHANNEL_4       4
#define PCA_CHANNEL_5       5
#define PCA_CHANNEL_6       6
#define PCA_CHANNEL_7       7
#define PCA_CHANNEL_8       8
#define PCA_CHANNEL_9       9
#define PCA_CHANNEL_10      10
#define PCA_CHANNEL_11      11
#define PCA_CHANNEL_12      12
#define PCA_CHANNEL_13      13
#define PCA_CHANNEL_14      14
#define PCA_CHANNEL_15      15

#define PWMA        PCA_CHANNEL_0
#define AIN1        PCA_CHANNEL_2
#define AIN2        PCA_CHANNEL_1
#define PWMB        PCA_CHANNEL_5
#define BIN1        PCA_CHANNEL_3
#define BIN2        PCA_CHANNEL_4
#define PWMC        PCA_CHANNEL_6
#define CIN2        PCA_CHANNEL_7
#define CIN1        PCA_CHANNEL_8

#define PWMD        PCA_CHANNEL_11
#define DIN1        6
#define DIN2        5

#define MOTORA       0
#define MOTORB       1
#define MOTORC       2
#define MOTORD       3

typedef enum {
    FORWARD  = 1,
    BACKWARD  ,
} DIR;
////-------IIC 控制------------
UBYTE DEV_ModuleInit(void);
void DEV_ModuleExit(void);

void DEV_I2C_Init(char addr);
void DEV_I2C_WriteByte(UBYTE reg, UBYTE value);
UBYTE DEV_I2C_ReadByte(UBYTE reg);

void DEV_Delay_ms(UDOUBLE xms);
void DEV_Delay_us(UDOUBLE xus);
//------PCA9685------------------
void PCA9685_Init(char addr);
void PCA9685_SetPWMFreq(UWORD freq);
void PCA9685_SetPwmDutyCycle(UBYTE channel, UWORD pulse);
void PCA9685_SetLevel(UBYTE channel, UWORD value);
//-------电机控制函数------------------
void Motor_Init(void);
void Motor_Run(UBYTE motor, DIR dir, UWORD speed);
void Motor_Stop(UBYTE motor);

//----机器人控制函数-------------------
void t_up(unsigned int speed,unsigned int t_time);     // 前进
void t_down(unsigned int speed,unsigned int t_time);   // 后退
void moveLeft(unsigned int speed,unsigned int t_time); // 左移
void moveRight(unsigned int speed,unsigned int t_time);// 右移
void turnLeft(unsigned int speed,unsigned int t_time); // 左转
void turnRight(unsigned int speed,unsigned int t_time);// 右转
void forward_Left(unsigned int speed,unsigned int t_time); // 前左斜
void forward_Right(unsigned int speed,unsigned int t_time);// 前右斜
void backward_Left(unsigned int speed,unsigned int t_time);// 后左斜
void backward_Right(unsigned int speed,unsigned int t_time);//后右斜
void t_stop(unsigned int t_time); // 停止
// 控制舵机角度
void set_servo_angle(unsigned int channel,float angle);

#endif
