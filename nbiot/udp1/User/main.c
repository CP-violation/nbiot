#include "system.h"
#include "SysTick.h"
#include "led.h"
#include "usart.h"
#include "key.h"
#include "adxl345.h"
#include "stdlib.h"
#include "BC20.h"
#include "HEXSTR.h"


unsigned char ReadAdxl345;	   //定时读取adxl345数据
unsigned char ErrorNum=0;   //记录错误次数
unsigned char CheckNum=0;   //检测次数
unsigned long ReportLater=0; //上报延时
unsigned long KeyLater=3;	 //按键延时计数

u8 min1=78;
u8 max1=82;
u8 heartrate;

u8 min2=95;
u8 max2=97;
u8 spo2;

extern BC20 BC20_Status;
u8 heart,blood,body_status;


//	void xuni(){
//		//心率 78-82
//		heartrate=rand()%(max1-min1)+min1;
//		printf("heartrate:%d\r\n",heartrate);
//		//血氧
//		spo2=rand()%(max2-min2)+min2;
//		printf("spo2:%d\r\n",heartrate);
//	}	

int main()
{
//	u8 i=0;

	u16 len;
    char struart1[BUFLEN];
    char lenstr[BUFLEN];
    char struart1hex[BUFLEN];
    char struart1OK[BUFLEN];
    char sendata[100];
    char Bodystr[100];

    char location[BUFLEN];          //存放数据经纬度用来发送
	char locationHEX[BUFLEN];          //存放数据经纬度用来发送
    
		
	volatile uint32_t time = 0; // ms 计时变量 
	unsigned char ReadAdxl345;	   //定时读取adxl345数据
	SysTick_Init(72);
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);  //中断优先级分组 分2组
	uart1_init(9600);
	uart2_init(115200);
  uart3_init(9600);
  LED_Init();		  	//初始化与LED连接的硬件接?
	KEY_Init();

//	if (SysTick_Config(SystemCoreClock / 1000))//设置24bit定时器 1ms中断一次
//    {
//        /* Capture error */
//        while (1);
//			printf("222");
//    }

	BUZZER = 1;
	delay_ms(100);
	BUZZER = 0;	//初始化

	
	Init_ADXL345();
	printf("3333");
	if(Single_Read_ADXL345(0X00)==0xe5)	
	{
		printf("ADXL345 OK!\r\n");
		delay_ms(200);
	}
	else
	{
		printf("ADXL345 Error!\r\n");
		delay_ms(3);	
	}	 
	GSM_LED =1;	//关闭LED指示
	
	
//    uart1_SendStr("init stm32L COM1 \r\n"); //打印信息
    //Uart2_SendStr("init stm32L COM2 \r\n"); //和NBIOT连接
    //Uart3_SendStr("init stm32L COM3 \r\n"); //用于其他TTL或者485
    while(BC20_Init());
    BC20_INITGNSS();
    BC20_PDPACT();
    BC20_ConUDP();
    delay_ms(2000);
	
	
	while(1)
	{		
		
		Clear_Buffer();
    Uart2_SendStr("AT+QGNSSRD=\"NMEA/RMC\"\r\n");
    delay_ms(2000);
//		BC20_Senddata("7",(u8 *)"I am OK");

        if(strstr((char *)buf_uart2.buf,"$GNRMC"))
        {
            memset(struart1,0,BUFLEN);
            memset(struart1hex,0,BUFLEN);	//清空
            memset(struart1OK,0,BUFLEN);	//清空
            memset(lenstr,0,BUFLEN);
            memset(location,0,BUFLEN);                  //清空location数据包缓存，保存经纬度的数据
            memset(locationHEX,0,BUFLEN); //清空locationHex数据包缓存，转换为hex 需要发送的真实数据
            sprintf(struart1,"%s",buf_uart2.buf+34);//数据接收 去掉前面的回显
            Clear_Buffer();

            strncpy(struart1OK,struart1,strlen(struart1)-8);   //去掉后面的回车和OK
            struart1OK[2]='P';

            strcpy((char*)(location+strlen((char*)location)),"GPS_lat:");//在HTTPTCPData中定义tcp包wei变量
            //将经度复制location变量中
            strncpy((char*)(location+strlen((char*)location)),&struart1[19],2);
            strncpy((char*)(location+strlen((char*)location)),".",1);
            strncpy((char*)(location+strlen((char*)location)),&struart1[21],2);
            strncpy((char*)(location+strlen((char*)location)),&struart1[24],4);
            strcpy((char*)(location+strlen((char*)location)),"&GPS_log:");//在HTTPTCPData中定义TCP包jing变量
            //将纬度复制location数组中
            strncpy((char*)(location+strlen((char*)location)),(char*)(&struart1[31]),3);
            strncpy((char*)(location+strlen((char*)location)),".",1);
            strncpy((char*)(location+strlen((char*)location)),(char*)(&struart1[34]),2);
            strncpy((char*)(location+strlen((char*)location)),(char*)(&struart1[37]),4);
			//printf("%s****%s\r\n",(char*)&struart1[21],(char*)&struart1[34]);
      memset(lenstr,0,BUFLEN);
		  memset(sendata,0,100);
		
		
 INI:		
		
//		time++;
//		if(time==200)
//		{
//			printf("8888/r/n");
//			time=0;
//			ReadAdxl345=1;
//		}

time=200;
while(time>0){
	time--;
	ReadAdxl345=1;
		if(ReadAdxl345==1){			
		ReadAdxl345= 0;
		ReadData_x();  						//三轴检测函数
		CheckNum++;
//			printf("X轴的值：%f\r\n",temp_X) ;

	
		delay_ms(100);
			 if((temp_X<550)||(temp_X>10000))        //方位值判断 查看正常次数
      {
        ErrorNum++;
      }
      if(CheckNum>=100)	  	//进行1000次处理
      {
//				xuni();
        if(KeyLater>=3)	  	//非按键下
        {
          if(ErrorNum>=1)	   //角度出现错误 10次出息1次情况
          {
           BUZZER = 1;	   //打开蜂鸣器
					 delay_ms(3);
					 ReportLater++;
						body_status=0;
						printf("body_status=0 摔倒  \r\n") ;
          }
          else
          {			
            BUZZER = 0;		//关闭蜂鸣器
						body_status=1;
						printf("body_status=1  正常\r\n",&BUZZER) ;	
						delay_ms(3);	
            ReportLater=0;		//上报延时计数
          }					
        }
        ErrorNum=0;		  //清空滤波计数
        CheckNum=0;	
      }
    }
		
	}	
			strcat(sendata,"&heart:");
			memset(Bodystr,0,100);

			sprintf(Bodystr,"%d",rand()%(max1-min1)+min1);
			strcat(sendata,Bodystr);
		
			strcat(sendata,"&blood:");
			sprintf(Bodystr,"%d",rand()%(max2-min2)+min2);
			strcat(sendata,Bodystr);
			
		// 1--正常 0--摔倒
			strcat(sendata,"&body_status:");
			sprintf(Bodystr,"%d",body_status);
			strcat(sendata,Bodystr);
		//sprintf(Bodystr,"%dihjHr);
		//sprintf(Bodystr,"%d",HSpo2);
		//sprintf(Bodystr,"%d",shuaidao);
			strcat(sendata,"#");
			strcat(location,sendata);
			sprintf(lenstr,"%d",strlen((char*)location));        //计数准备发送的数据
            printf("lenstr=%s\r\n",lenstr);
			Str2Hex(location,locationHEX);
            BC20_SenddataHEX((u8 *)lenstr,(u8 *)locationHEX);//
            printf((char *)location);
            printf("\r\n");

        }
		
				

				//15s内老人摔倒没有站起来
	if(ReportLater>=3)	//15s
    {
      GSM_LED = 0; //打开指示灯，发送gps定位信息
	  delay_ms(3);	

	  printf("声光报警",GSM_LED);
			
      GSM_LED =1;		//led关闭
	  delay_ms(3);	
      ReportLater=0;	//上报标志清空
      KeyLater=0;	//按键清零延时处理
	  goto INI;
    }
    if(key==0)		 //按键处理
    {
      delay_ms(3);  	//按键消抖动
      if(key ==0)		 //按键处理
      {
        ReportLater=0;	  //按键延时上报
        BUZZER = 0;		 //关闭蜂鸣器
		printf("取消报警  \r\n",&BUZZER) ;	
		delay_ms(3);
        KeyLater=0;		//按键延时处理
      }
//		goto INI;
    }
		
	}

		
}
