# 3.5" Display with ILI driver without framebuffer
import ILI9488 as display
import time
import io

if __name__=='__main__':

    LCD = display.LCD_3inch5()
    LCD.bl_ctrl(50)
    header = bytearray(54)
    pic = open("cat16.bmp", "rb")  ## warning, cat16 has no valid bmp header
#    pic16 = open("hamster16.bmp", "wb")
    header = pic.read(54)
    
#    pic16.write(header)
    for y in range(320):
        buf = pic.read(480*2)
        LCD.rect(0, 320-1-y, 480, 1, buf)
#        pic16.write(buf)
    pic.close
#    pic16.close
    
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
            LCD.bl_ctrl(X_Point * 100 // 480)
            time.sleep(0.1)
        else:
            time.sleep(0.1)
           


