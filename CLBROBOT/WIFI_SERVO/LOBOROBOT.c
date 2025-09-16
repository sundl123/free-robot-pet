#include "LOBOROBOT.h"
#include <math.h>
#include <stdio.h>
#include <time.h>

UBYTE DEV_ModuleInit(void)
{
    if(wiringPiSetupGpio() < 0) { //use BCM2835 Pin number table
        DEBUG("set wiringPi lib failed	!!! \r\n");
        return 1;
    } else {
        DEBUG("set wiringPi lib success  !!! \r\n");
    }

    return 0;
}

void DEV_ModuleExit(void)
{

}
void DEV_I2C_Init(char addr)
{
    fd = wiringPiI2CSetup(addr);
}

void DEV_I2C_WriteByte(UBYTE reg, UBYTE value)
{
    int ref;
    ref = wiringPiI2CWriteReg8(fd, (int)reg, (int)value);
    while(ref != 0) {
        ref = wiringPiI2CWriteReg8 (fd, (int)reg, (int)value);
        if(ref == 0)
            break;
    }
}

UBYTE DEV_I2C_ReadByte(UBYTE reg)
{
    return wiringPiI2CReadReg8(fd, reg);
}

void DEV_Delay_ms(uint32_t xms)
{
    delay(xms);
}

void DEV_Delay_us(uint32_t xus)
{
    int j;
    for(j=xus; j > 0; j--);
}

static void PCA9685_WriteByte(UBYTE reg, UBYTE value)
{
    DEV_I2C_WriteByte(reg, value);
}


static UBYTE PCA9685_ReadByte(UBYTE reg)
{
    return DEV_I2C_ReadByte(reg);
}


static void PCA9685_SetPWM(UBYTE channel, UWORD on, UWORD off)
{
    PCA9685_WriteByte(LED0_ON_L + 4*channel, on & 0xFF);
    PCA9685_WriteByte(LED0_ON_H + 4*channel, on >> 8);
    PCA9685_WriteByte(LED0_OFF_L + 4*channel, off & 0xFF);
    PCA9685_WriteByte(LED0_OFF_H + 4*channel, off >> 8);
}


void PCA9685_Init(char addr)
{
    DEV_I2C_Init(addr);
    DEV_I2C_WriteByte(MODE1, 0x00);
}

void PCA9685_SetPWMFreq(UWORD freq)
{
    freq *= 0.9;  // Correct for overshoot in the frequency setting (see issue #11).
    double prescaleval = 25000000.0;
    prescaleval /= 4096.0;
    prescaleval /= freq;
    prescaleval -= 1;
    DEBUG("prescaleval = %lf\r\n", prescaleval);

    UBYTE prescale = floor(prescaleval + 0.5);
    DEBUG("prescaleval = %lf\r\n", prescaleval);

    UBYTE oldmode = PCA9685_ReadByte(MODE1);
    UBYTE newmode = (oldmode & 0x7F) | 0x10; // sleep

    PCA9685_WriteByte(MODE1, newmode); // go to sleep
    PCA9685_WriteByte(PRESCALE, prescale); // set the prescaler
    PCA9685_WriteByte(MODE1, oldmode);
    DEV_Delay_ms(5);
    PCA9685_WriteByte(MODE1, oldmode | 0x80);  //  This sets the MODE1 register to turn on auto increment.
}

void PCA9685_SetPwmDutyCycle(UBYTE channel, UWORD pulse)
{
    PCA9685_SetPWM(channel, 0, pulse * (4096 / 100) - 1);
}

void PCA9685_SetLevel(UBYTE channel, UWORD value)
{
    if (value == 1)
        PCA9685_SetPWM(channel, 0, 4095);
    else
        PCA9685_SetPWM(channel, 0, 0);
}

void Motor_Init(void)
{
    PCA9685_Init(0x40);
    PCA9685_SetPWMFreq(50);
    wiringPiSetup();
    pinMode(DIN1,OUTPUT);	
    pinMode(DIN2,OUTPUT);   
}

void Motor_Run(UBYTE motor, DIR dir, UWORD speed)
{
    if(speed > 100)
        speed = 100;

    if(motor == MOTORA)
     {
        PCA9685_SetPwmDutyCycle(PWMA, speed);
        if(dir == FORWARD) 
        {
            PCA9685_SetLevel(AIN1, 0);
            PCA9685_SetLevel(AIN2, 1);
        } 
        else 
        {
            PCA9685_SetLevel(AIN1, 1);
            PCA9685_SetLevel(AIN2, 0);
        }
    } 
    else if(motor == MOTORB) 
    {
        PCA9685_SetPwmDutyCycle(PWMB, speed);
        if(dir == FORWARD) 
        {
            PCA9685_SetLevel(BIN1, 1);
            PCA9685_SetLevel(BIN2, 0);
        } 
        else 
        {
            PCA9685_SetLevel(BIN1, 0);
            PCA9685_SetLevel(BIN2, 1);
        }
    }
    else if(motor == MOTORC)
    {
		PCA9685_SetPwmDutyCycle(PWMC,speed);
		if(dir == FORWARD)
		{
			PCA9685_SetLevel(CIN1,1);
			PCA9685_SetLevel(CIN2,0);
		}
		else
		{
			PCA9685_SetLevel(CIN1,0);
			PCA9685_SetLevel(CIN2,1);
		}
	}
	else if(motor == MOTORD)
	{
		PCA9685_SetPwmDutyCycle(PWMD,speed);
		if(dir == FORWARD)
		{
			digitalWrite(DIN1,0);
			digitalWrite(DIN2,1);
		}
		else
		{
			digitalWrite(DIN1,1);
			digitalWrite(DIN2,0);
		}
	}
	else
	{
		DEBUG("Input port error!\r\n");
	}	
}
	
void Motor_Stop(UBYTE motor)
{
    if(motor == MOTORA) 
    {
        PCA9685_SetPwmDutyCycle(PWMA, 0);
    } 
    else if(motor == MOTORB)
    {
        PCA9685_SetPwmDutyCycle(PWMB, 0);
    }
    else if(motor == MOTORC)
    {
		PCA9685_SetPwmDutyCycle(PWMC, 0);
	}
	else if(motor == MOTORD)
	{
		PCA9685_SetPwmDutyCycle(PWMD, 0);
	}
	else
	{
		DEBUG("Input port error!\r\n");
	}
}
// ----机器人前进-----------
void t_up(unsigned int speed,unsigned int t_time)
{
	Motor_Run(MOTORA,FORWARD,speed);
	Motor_Run(MOTORB,FORWARD,speed);
	Motor_Run(MOTORC,FORWARD,speed);
	Motor_Run(MOTORD,FORWARD,speed);
	delay(t_time);
}
// 后退
void t_down(unsigned int speed,unsigned int t_time)
{
    Motor_Run(MOTORA,BACKWARD,speed);
    Motor_Run(MOTORB,BACKWARD,speed);
    Motor_Run(MOTORC,BACKWARD,speed);
    Motor_Run(MOTORD,BACKWARD,speed);
    delay(t_time);
}
// 左移
void moveLeft(unsigned int speed,unsigned int t_time)
{
    Motor_Run(MOTORA,BACKWARD,speed);
    Motor_Run(MOTORB,FORWARD,speed);
    Motor_Run(MOTORC,FORWARD,speed);
    Motor_Run(MOTORD,BACKWARD,speed);
    delay(t_time);
}
// 右移
void moveRight(unsigned int speed,unsigned int t_time)
{
    Motor_Run(MOTORA,FORWARD,speed);
    Motor_Run(MOTORB,BACKWARD,speed);
    Motor_Run(MOTORC,BACKWARD,speed);
    Motor_Run(MOTORD,FORWARD,speed);
    delay(t_time);
}
// 左转
void turnLeft(unsigned int speed,unsigned int t_time)
{
    Motor_Run(MOTORA,BACKWARD,speed);
    Motor_Run(MOTORB,FORWARD,speed);
    Motor_Run(MOTORC,BACKWARD,speed);
    Motor_Run(MOTORD,FORWARD,speed);
    delay(t_time);
}
// 右转
void turnRight(unsigned int speed,unsigned int t_time)
{
    Motor_Run(MOTORA,FORWARD,speed);
    Motor_Run(MOTORB,BACKWARD,speed);
    Motor_Run(MOTORC,FORWARD,speed);
    Motor_Run(MOTORD,BACKWARD,speed);
    delay(t_time);
}
// 前左斜
void forward_Left(unsigned int speed,unsigned int t_time)
{
    Motor_Stop(MOTORA);
    Motor_Run(MOTORB,FORWARD,speed);
    Motor_Run(MOTORC,FORWARD,speed);
    Motor_Stop(MOTORD);
    delay(t_time);
}
// 前右斜
void forward_Right(unsigned int speed,unsigned int t_time)
{
    Motor_Run(MOTORA,FORWARD,speed);
    Motor_Stop(MOTORB);
    Motor_Stop(MOTORC);
    Motor_Run(MOTORD,FORWARD,speed);
    delay(t_time);
}
// 后左斜
void backward_Left(unsigned int speed,unsigned int t_time)
{
    Motor_Run(MOTORA,BACKWARD,speed);
    Motor_Stop(MOTORB);
    Motor_Stop(MOTORC);
    Motor_Run(MOTORD,BACKWARD,speed);
    delay(t_time); 
}

// 后右斜
void backward_Right(unsigned int speed,unsigned int t_time)
{
    Motor_Stop(MOTORA);
    Motor_Run(MOTORB,BACKWARD,speed);
    Motor_Run(MOTORC,BACKWARD,speed);
    Motor_Stop(MOTORD);
    delay(t_time);
}
// 停止
void t_stop(unsigned int t_time)
{
	Motor_Stop(MOTORA);
	Motor_Stop(MOTORB);
	Motor_Stop(MOTORC);
	Motor_Stop(MOTORD);
	delay(t_time);
}

// 控制舵机角度
void set_servo_angle(unsigned int channel,float angle)
{
    uint16_t angle_t = 4096*((angle*11)+500)/20000;
    PCA9685_SetPWM(channel,0,angle_t);
    
}
