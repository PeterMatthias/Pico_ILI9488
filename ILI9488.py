# 3.5" Display with ILI driver without framebuffer
from machine import Pin,SPI,PWM
import time
import io

LCD_DC   = 8
LCD_CS   = 9
LCD_SCK  = 10
LCD_MOSI = 11
LCD_MISO = 12
LCD_BL   = 13
LCD_RST  = 15
TP_CS    = 16
TP_IRQ   = 17

WIDTH = 480
HEIGHT = 320

buf = bytearray(WIDTH * 2)

class LCD_3inch5():

    def __init__(self):
        self.RED   =   0xf800 
        self.GREEN =   0x07E0
        self.BLUE  =   0x001f
        self.YELLOW =  0xffe0
        self.WHITE =   0xffff
        self.BLACK =   0x0000
        
        self.width = WIDTH #480
        self.height = HEIGHT #160      
        
        self.cs = Pin(LCD_CS,Pin.OUT)
        self.rst = Pin(LCD_RST,Pin.OUT)
        self.dc = Pin(LCD_DC,Pin.OUT)
        
        self.tp_cs =Pin(TP_CS,Pin.OUT)
        self.irq = Pin(TP_IRQ,Pin.IN)
        
        self.cs(1)
        self.dc(1)
        self.rst(1)
        self.tp_cs(1)
        self.spi = SPI(1,60_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
        self.init_display()
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        #self.spi.write(bytearray([0X00]))
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep_ms(5)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(5)
        self.write_cmd(0x21) # display inversion on
        self.write_cmd(0xC2) # power control 3
        self.write_data(0x33) 
        self.write_cmd(0XC5)  # VCOM control 1
        self.write_data(0x00)
        self.write_data(0x1e)
        self.write_data(0x80)
        self.write_cmd(0xB1) # frame rate control
        self.write_data(0xB0)
        self.write_cmd(0x36) # memory access control
        self.write_data(0x28)
        self.write_cmd(0XE0) # pgamctrl
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x04)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x3a)
        self.write_data(0x56)
        self.write_data(0x4d)
        self.write_data(0x03)
        self.write_data(0x0a)
        self.write_data(0x06)
        self.write_data(0x30)
        self.write_data(0x3e)
        self.write_data(0x0f)
        self.write_cmd(0XE1) # ngamctrl
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x01)
        self.write_data(0x11)
        self.write_data(0x06)
        self.write_data(0x38)
        self.write_data(0x34)
        self.write_data(0x4d)
        self.write_data(0x06)
        self.write_data(0x0d)
        self.write_data(0x0b)
        self.write_data(0x31)
        self.write_data(0x37)
        self.write_data(0x0f)
        self.write_cmd(0X3A) # interface pixel format
        self.write_data(0x55)
        self.write_cmd(0x11) # sleep put
        time.sleep_ms(120)
        self.write_cmd(0x29) # display on
        
        self.write_cmd(0xB6) # display function control
        self.write_data(0x00)
        self.write_data(0x62)
        
        self.write_cmd(0x36) # memory access control
        self.write_data(0x28)
        
    def bl_ctrl(self,duty): # back light control
        pwm = PWM(Pin(LCD_BL))
        pwm.freq(1000)
        if(duty>=100):
            pwm.duty_u16(65535)
        else:
            pwm.duty_u16(655*duty)

    def draw_hline(self, x, y, w, color): #
        self.write_cmd(0x2A)
        self.write_data(x >> 8)
        self.write_data(x & 0xff)
        self.write_data((x+w-1) >> 8)
        self.write_data((x+w-1) & 0xff)
 
        self.write_cmd(0x2B)
        self.write_data(y >> 8)
        self.write_data(y & 0xff)
        self.write_data(y >> 8)
        self.write_data(y & 0xff)
        
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        #self.spi.write(bytearray([0X00]))
        for i in range(0, w):
            self.spi.write(color.to_bytes(2, 0))
#        for i in range(0, w*2):
#            buf[i] = color >> 8
#            buf[i+1] = color && 0xff
        
        self.cs(1)
   
    def draw_vline(self, x, y, h, color): #
        self.write_cmd(0x2A)
        self.write_data(x >> 8)
        self.write_data(x & 0xff)
        self.write_data(x >> 8)
        self.write_data(x & 0xff)
 
        self.write_cmd(0x2B)
        self.write_data(y >> 8)
        self.write_data(y & 0xff)
        self.write_data((y + h - 1) >> 8)
        self.write_data((y + h - 1) & 0xff)
        
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        #self.spi.write(bytearray([0X00]))
        for i in range(0, h):
            self.spi.write(color.to_bytes(2, 0))
        self.cs(1)
       
    def fill_rect(self, x, y, w, h, color):
        self.write_cmd(0x2A)
        self.write_data(x >> 8)
        self.write_data(x & 0xff)
        self.write_data((x + w - 1) >> 8)
        self.write_data((x + w - 1) & 0xff)
 
        self.write_cmd(0x2B)
        self.write_data(y >> 8)
        self.write_data(y & 0xff)
        self.write_data((y + h - 1) >> 8)
        self.write_data((y + h - 1) & 0xff)
        
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        #self.spi.write(bytearray([0X00]))
#        for i in range(h):
#            for j in range(w):
#                self.spi.write(color.to_bytes(2, 0))

        for i in range(0, w*2, 2):
            buf[i] = color >> 8
            buf[i+1] = color & 0xff
        for j in range(h):
            self.spi.write(buf[:w*2])
        self.cs(1)
    
    def outline_rect(self, x, y, w, h, color):
        self.draw_hline(x, y, w, color)
        self.draw_hline(x, y+h, w, color)
        self.draw_vline(x, y, h, color)
        self.draw_vline(x+w, y, h, color)

    def rect(self, x, y, w, h, data): #
        self.write_cmd(0x2A)
        self.write_data(x >> 8)
        self.write_data(x & 0xff)
        self.write_data((x + w - 1) >> 8)
        self.write_data((x + w - 1) & 0xff)
 
        self.write_cmd(0x2B)
        self.write_data(y >> 8)
        self.write_data(y & 0xff)
        self.write_data((y + h - 1) >> 8)
        self.write_data((y + h - 1) & 0xff)

#        self.write_cmd(0x2B)
#        self.cs(1)
#        self.dc(1)
#        self.cs(0)
        #self.spi.write(bytearray([0X00]))
#        self.spi.write(bytearray([0X00]))
#        self.spi.write(bytearray([y]))
#        self.spi.write(bytearray([0X00]))
#        self.spi.write(bytearray([y]))
#        self.spi.write(y.to_bytes(1, 'big' ))
#        self.cs(1)
        
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        #self.spi.write(bytearray([0X00]))
        self.spi.write(data)
        self.cs(1)
        
    def setfont(self, font):
        self.font=font

    def text(self, str, x, y, color):       
        for i in (str):
            glyph, h, w = self.font.get_ch(i)
            
#             m = 0
#             for j in range(h):
#                 for k in range(w):
#                     if k % 8 == 0:
#                         c = glyph[m]
#                         m += 1
#                     if (c >> (7-(k % 8))) % 2:
#                         self.draw_hline(x + k, y + j, 1, color)
#             x += w + 1

            l = 0
            m = 0
            buf = bytearray(w * h * 2)
            for j in range(h):
                for k in range(w):
                    if k % 8 == 0:
                        c = glyph[m]
                        m += 1
                    if (c >> (7-(k % 8))) % 2:
                        buf[l] = color >> 8
                        buf[l + 1] = color & 0xff
                    else:
                        buf[l] = 0xff
                        buf[l + 1] = 0xff
                    l += 2
            self.rect(x, y, w, h, buf)
            x += w + 1

#            print(len(glyph))
        
    def touch_get(self): 
        if self.irq() == 0:
            self.spi = SPI(1,5_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
            self.tp_cs(0)
            X_Point = 0
            Y_Point = 0
            for i in range(0,3):
                self.spi.write(bytearray([0XD0]))
                Read_date = self.spi.read(2)
                time.sleep_us(10)
                X_Point=X_Point+(((Read_date[0]<<8)+Read_date[1])>>3)
                
                self.spi.write(bytearray([0X90]))
                Read_date = self.spi.read(2)
                Y_Point=Y_Point+(((Read_date[0]<<8)+Read_date[1])>>3)

            X_Point=X_Point/3
            Y_Point=Y_Point/3
            
            self.tp_cs(1) 
            self.spi = SPI(1,60_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
            Result_list = [X_Point,Y_Point]
            #print(Result_list)
            return(Result_list)



