/**
 SPI HOMEWORK2 , LABWORK2 (SAME PROGRAM)
 */

/* @section  I N C L U D E S */
#include "at89c5131.h"
#include "stdio.h"
#define LCD_data  P2	    					// LCD Data port
#define sample 1
void SPI_Init();
void LCD_Init();
void Timer_Init();
void LCD_DataWrite(char dat);
void LCD_CmdWrite(char cmd);
void LCD_StringWrite(char * str, unsigned char len);
void LCD_Ready();
void sdelay(int delay);
void display_value();
void display_voltage_lcd();
void delay_ms(int delay);
char int_to_string(int val);
void sample_data(int no_of_samples);
void binary_to_ascii(int binary);
sbit CS_BAR = P3^4;									// Chip Select for the ADC
sbit FS = P3^5;									// Frame Select for the ADC
sbit LCD_rs = P0^0;  								// LCD Register Select
sbit LCD_rw = P0^1;  								// LCD Read/Write
sbit LCD_en = P0^2;  								// LCD Enable
sbit LCD_busy = P2^7;								// LCD Busy Flag
sbit LED = P1^7;
sbit ONULL = P1^0;
bit transmit_completed= 0;							// To check if spi data transmit is complete
bit offset_null = 0;								// Check if offset nulling is enabled
bit roundoff = 0;
bit send_data= 0;							// To check if spi data transmit is complete
bit going_up= 1;	

unsigned int  voltage= 0;


unsigned char serial_data;
unsigned char data_high;
unsigned char data_low;
unsigned char data_msb=0;
unsigned char data_lsb=0;
unsigned char count=0, i=0;
float fweight=0;
int counter=0;
char state=0;
unsigned char voltage_display_ascii[4];

/**

 * FUNCTION_INPUTS:  P1.5(MISO) serial input  
 * FUNCTION_OUTPUTS: P1.7(MOSI) serial output
 *                   P1.4(SSbar)
                     P1.6(SCK)
 */
 
void main(void)
{
	P3 = 0x00;
	CS_BAR = 1; 
	FS = 1;

	SPI_Init();
	Timer_Init();
	
	while(1)
	{
		if(send_data){
			
		CS_BAR = 0;                 							// falling edge of CS bar
		FS = 0;
		
		data_lsb = voltage;
		data_msb = voltage>>8;
		SPDAT= data_msb;											// first 4 bits will be address of the channel. next 4 can be anything
		while(!transmit_completed);								// wait for the transmit complete flag	
		transmit_completed = 0;    								// make the flag 0
		
		SPDAT =data_lsb;											// here can send anything. doesnt matter. it will not read the address till the next cycle starts. or eoc becomes low and high again.
																			//this we are sending because we are receiving 8 bits, so have to send something. 
		while(!transmit_completed);	
		transmit_completed = 0; 
		FS = 1;
		CS_BAR = 1;    
		send_data=0;
		}
	}

}
send_SPI (char transmit_data){

	SPDAT = transmit_data;
		while(!transmit_completed);								// wait for the transmit complete flag	
		//data_save_high = serial_data;  							// save the 
		transmit_completed = 0;    								// make the flag 0
		SPDAT =0x00;											// here can send anything. doesnt matter. it will not read the address till the next cycle starts. or eoc becomes low and high again.
		
																//this we are sending because we are receiving 8 bits, so have to send something. 
		while(!transmit_completed);	
//		data_save_low = serial_data;
		transmit_completed = 0; 

	return;
}
/**
 * FUNCTION_PURPOSE:interrupt
 * FUNCTION_INPUTS: void
 * FUNCTION_OUTPUTS: transmit_complete is software transfert flag
 */
void it_SPI(void) interrupt 9 /* interrupt address is 0x004B, (Address -3)/8 = interrupt no.*/
{
	switch	( SPSTA )         /* read and clear spi status register */
	{
		case 0x80:	
			serial_data=SPDAT;   /* read receive data */
			transmit_completed=1;/* set software flag */
 		break;

		case 0x10:
			
		break;
	
		case 0x40:
		break;
	}
}

void timer0_ISR (void) interrupt 1
{
			TR0 = 0;
		
		TH0 |= 0xF4;   //for  6/2^12
		TL0 |= 0x8E;	// for  6/2^12
		send_data = 1;
		TR0 =1;
	
	if (going_up)
	{
		if (voltage<4095){
			voltage++;
		}
			else {
		
		going_up=0;
	}
	}
	else {
			if (voltage>0){
			voltage--;
		}
			else {
		
		going_up=1;
	}
	
	}
	


	return;

}


/**

 * FUNCTION_INPUTS:  P1.5(MISO) serial input  
 * FUNCTION_OUTPUTS: P1.7(MOSI) serial output
 *                   P1.4(SSbar)
                     P1.6(SCK)
 */ 
void SPI_Init()
{
	CS_BAR = 1;	                  	// DISABLE ADC SLAVE SELECT-CS 
	SPCON |= 0x20;               	 	// P1.1(SSBAR) is available as standard I/O pin 
	SPCON |= 0x01;                	// Fclk Periph/4 AND Fclk Periph=12MHz ,HENCE SCK IE. BAUD RATE=3000KHz 
	SPCON |= 0x10;               	 	// Master mode 
	SPCON |= 0x08;               	// CPOL=1; transmit mode example|| SCK is 0 at idle state
	SPCON &= ~0x04;                	// CPHA=0; transmit mode example 
	IEN1 |= 0x04;                	 	// enable spi interrupt 
	EA=1;                         	// enable interrupts 
	SPCON |= 0x40;                	// run spi;ENABLE SPI INTERFACE SPEN= 1 

//	IPH0 |=0x10;
//	IPL0 |=0x10;
}

void Timer_Init()
{
	// Set Timer0 to work in up counting 16 bit mode. Counts upto 
	// 65536 depending upon the values of TH0 and TL0
	// The timer counts 65536 processor cycles. A processor cycle is 
	// 12 clocks. FOr 24 MHz, it takes 65536/2 uS to overflow
    
    TH0 |= 0xF4;   //for  5000
    TL0 |= 0x8E;	// for 5000
    
    TMOD|=0X01;
   	EA=1;
    ET0=1;
    TR0=1;
		
	//Initialize TH0
	//Initialize TL0
	//Configure TMOD 
	//Set ET0
	//Set TR0
}
/**
 * FUNCTION_PURPOSE:LCD Initialization
 * FUNCTION_INPUTS: void
 * FUNCTION_OUTPUTS: none
 */

/**
 * FUNCTION_PURPOSE: A delay of 15us for a 24 MHz crystal
 * FUNCTION_INPUTS: void
 * FUNCTION_OUTPUTS: none
 */
void sdelay(int delay)
{
	char d=0;
	while(delay>0)
	{
		for(d=0;d<5;d++);
		delay--;
	}
}

/**
 * FUNCTION_PURPOSE: A delay of around 1000us for a 24MHz crystel
 * FUNCTION_INPUTS: void
 * FUNCTION_OUTPUTS: none
 */
void delay_ms(int delay)
{
	int d=0;
	while(delay>0)
	{
		for(d=0;d<382;d++);
		delay--;
	}
}