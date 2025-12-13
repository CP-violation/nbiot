#ifndef __USART_H
#define __USART_H
#include "stdio.h"	
//#include "delay.h"
#include "system.h"
#include "SysTick.h"
#include "stm32f10x.h"
//#define u8 int8_t
//#define u16 int16_t
//#define u32 int32_t

#define BUFLEN 256      //数组缓存大小
typedef struct _UART_BUF
{
    char buf [BUFLEN+1];               
    unsigned int index ;
}UART_BUF;

void uart1_init(u32 bound);     //串口初始化
void uart2_init(u32 bound);
void uart3_init(u32 bound);
void Uart1_SendStr(char*SendBuf);   //字符串发送
void Uart2_SendStr(char*SendBuf);
void Uart3_SendStr(char*SendBuf);


extern UART_BUF buf_uart1;     //CH340
extern UART_BUF buf_uart2;     //NBIOT
extern UART_BUF buf_uart3;     //TTL
extern u8 Rec_flag;
#endif




