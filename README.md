# PomodoroPebble
The PomodoroPebble is a project that is meant to help everyone focus. The Pomodoro technique is often hailed as one of the greatest studying methods, providng breaks and long working periods to help productivity but is hasrd to implement in theory. As an avid user of the Pomodoro method, I would often end up distracting myself with the online technology online to use a Pomodoro timer, which is why I made a mechanical alternate. 

This is what the PomodoroPebble looks like:

<img width="1333" height="790" alt="image" src="https://github.com/user-attachments/assets/5e19a795-0569-44d8-abdc-530b6d2c7079" />
<img width="1360" height="795" alt="image" src="https://github.com/user-attachments/assets/a88aa6a3-5ae2-43cb-bbf3-517190ccb1a7" />

This is the PCB:
<img width="436" height="614" alt="image" src="https://github.com/user-attachments/assets/27851d74-383c-4d8f-a313-00fb67bbcfd7" />
<img width="719" height="661" alt="image" src="https://github.com/user-attachments/assets/0607b990-133c-4f51-8f39-a57de2c0146c" />

The case will fit together with glue and magnets to ensure reopenability and easy access to the internals.

BOM:
Reference	Qty	Value	DNP	Exclude from BOM	Exclude from Board	Footprint	Datasheet
D1,D2,D3,D4	4	RGB LED For Fun				LED_SMD:LED_SK6812MINI_PLCC4_3.5x3.5mm_P1.75mm	https://cdn-shop.adafruit.com/product-files/2686/SK6812MINI_REV.01-1-2.pdf
J1	1	OLED Screen Connector				OLED screen:SSD1306-0.91-OLED-4pin-128x32	~
SW1	1	Start/Stop				Button_Switch_Keyboard:SW_Cherry_MX_1.00u_PCB	~
SW2	1	Reset				Button_Switch_Keyboard:SW_Cherry_MX_1.00u_PCB	~
U2	1	XIAO-RP2040-DIP				OPL:XIAO-RP2040-DIP	
