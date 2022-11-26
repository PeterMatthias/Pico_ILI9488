# 3.5" Display with ILI driver without framebuffer
import ILI9488 as display
import time
import arial10 as font
        
if __name__=='__main__':

    LCD = display.LCD_3inch5()
    LCD.setfont(font)
    LCD.bl_ctrl(50)
    LCD.fill_rect(0, 0, 480, 320, LCD.WHITE)
    LCD.fill_rect(140, 5, 200, 30,LCD.RED)
    LCD.text("Raspberry Pi Pico",170,17,LCD.WHITE)
    
#    color= 0x0020   # r#0x0800, g=0x0020, b=0x0000
#    for y in range(0, 200):
#        LCD.draw_hline( 0, y, 200, color)
#        color += 0x20
    
#    display_color = 0x001F
    LCD.text("3.5' IPS LCD TEST",170,57,LCD.BLACK)
#    for i in range(0,12):      
#        LCD.fill_rect(i*30+60,80,30,50,(display_color))
#        display_color = display_color << 1
    red = 0x0
    green = 0x0
    blue = 0x0   
    for i in range(0x80):
        LCD.draw_hline(0, 80+i, 120, red)
        LCD.draw_hline(120, 80+i, 120, green)
        LCD.draw_hline(240, 80+i, 120, blue)
        LCD.draw_hline(360, 80+i, 120, red + green + blue)
        if i % 2:
            green += 0x20
            if i % 4 == 3:
                red += 0x800
                blue += 0x1
    LCD.text("Button0",20,255,LCD.RED)
    LCD.text("Button1",150,255,LCD.GREEN)
    LCD.text("Button2",270,255,LCD.BLUE)
    LCD.text("Button3",400,255,LCD.BLACK)
    while True:      
        get = LCD.touch_get()
        update= 0xf
        if get != None: 
            X_Point = int((get[1]-430)*480/3270)
            if(X_Point>480):
                X_Point = 480
            elif X_Point<0:
                X_Point = 0
            Y_Point = 320-int((get[0]-430)*320/3270)
            if(Y_Point>220):
                if(X_Point<120):
                    LCD.outline_rect(10,220,100,80,LCD.RED)
                    update = 1
#                    LCD.text("Button0",20,270,LCD.WHITE)
                    LCD.bl_ctrl(10)
                elif(X_Point<240):
                    LCD.outline_rect(130,220,100,80,LCD.RED)
                    update = 2
#                    LCD.text("Button1",150,270,LCD.WHITE)
                    LCD.bl_ctrl(40)
                elif(X_Point<360):
                    LCD.outline_rect(250,220,100,80,LCD.RED)
                    update = 4
#                    LCD.text("Button2",270,270,LCD.WHITE)
                    LCD.bl_ctrl(70)
                else:
                    LCD.outline_rect(370,220,100,80,LCD.RED)
                    update = 8
#                    LCD.text("Button3",400,270,LCD.WHITE)
                    LCD.bl_ctrl(100)
#            LCD.fill_rect(0, 220, LCD.width, 80, LCD.WHITE)
        else:
            if update %2:
                LCD.outline_rect(10,220,100,80,LCD.BLACK)
            if update // 2 % 2:
                LCD.outline_rect(130,220,100,80,LCD.BLACK)
            if update // 4 % 2:
                LCD.outline_rect(250,220,100,80,LCD.BLACK)
            if update // 8 % 2:
                LCD.outline_rect(370,220,100,80,LCD.BLACK)
            update = 0
            time.sleep(0.1)
           


