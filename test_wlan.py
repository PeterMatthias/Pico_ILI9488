# Version 2022-12-02
# Timezone gives correct date
import ujson
import ntptime
import network
import utime
import urequests
#import uasyncio as asyncio
import network
import socket
import gc

import freesans20 as font
import ILI9488 as display
from secrets import wlan_ssid, wlan_pwd, lat, lon, openweathermap_api_key

request_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweathermap_api_key}&lang=DE"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    tries = 20
    while tries >0:
        tries -=1
        wlan.connect(wlan_ssid, wlan_pwd)
 #       utime.sleep(1)
        stat = wlan.status()
        while stat == network.STAT_CONNECTING:
            LCD.text('Verbinde .  ', 100, 100, LCD.RED)
            utime.sleep(0.1)
            LCD.text("Verbinde ..   ", 100, 100, LCD.RED)
            utime.sleep(0.1)
            LCD.text("Verbinde ...", 100, 100, LCD.RED)
            utime.sleep(0.1)
            stat = wlan.status()
        if stat == network.STAT_GOT_IP:
            tries = 0
            LCD.text("Verbunden!", 100, 100, LCD.BLACK)
            status = wlan.ifconfig()
            print( f"Ip = {status[0]}")
        if stat == network.STAT_WRONG_PASSWORD:
            print( 'wrong password')
        if stat == network.STAT_NO_AP_FOUND:
            print( 'NO_AP_FOUND')
        else:
            print(f'status={stat}')
#            print(stat)
#        log.value("")
    
def clock():
    gc.collect()

    days = ('Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag',
            'Sonntag')
    months = ('Jan', 'Feb', 'Maerz', 'April', 'Mai', 'Juni', 'Juli',
              'Aug', 'Sept', 'Okt', 'Nov', 'Dez')
    
    ntptime.settime()
    
    weather_decsription_display = ""
    weather_temp_display = ""
    
    seconds = 0
    timeoffset = 0
    
    while True:
        if seconds == 0:
            _, _, host, path = request_url.split('/', 3)
            addr = socket.getaddrinfo(host, 80)[0][-1]
            s = socket.socket()
            s.connect(addr)
#            s.send(b'GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host))
            s.send(b'GET /%s HTTP/1.0\r\n\r\n' % (path))
            while True:
                data = s.read()
                if data:
                    data_new = str(data, 'utf8')
                    _, data = data_new.split('{', 1)
#                    print(data)
                    weather_data = ujson.loads("{" + data)  
                    
                    timeoffset = int(weather_data["timezone"]) // 3600
#                    LCD.fill_rect(100, 200, 200, 40, LCD.BLUE)               
                    LCD.text(f"In {weather_data["name"]} ist es {weather_data["weather"][0]["description"]}.", 100, 200, LCD.RED)
                    LCD.text(f"Temp: {round(weather_data["main"]["temp"] - 273.15, 1)} Grad C.", 100, 220, LCD.RED)
                else:
                    break
            s.close()            
            seconds = 6000

        t = utime.localtime()
        time = t[3] + timeoffset
        dateoffset = time // 24
        time %= 24
        date = t[2] + dateoffset
        month = t[1]
        year = t[0]
        weekday = days[(t[6] + dateoffset) % 7]
        
        end_of_the_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        if year % 4 == 0 and year % 100 != 0: # leap year
            end_of_the_month = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        
        if date == 0:
            month -= 1
            date = end_of_the_month[month - 1]
            if month == 0:
                year -= 1
                month = 12
        
        if date > end_of_the_month[month - 1]:
            month += 1
            date = 1
            if month > 12:
                year += 1
                month = 1
        
#        LCD.fill_rect(100, 270, 200, 30, LCD.RED)
        LCD.text(f'{time:02d}:{t[4]:02d}:{t[5]:02d} Uhr', 100, 270, LCD.BLACK)
        LCD.text(f'{weekday} {date}. {months[month - 1]} {year}', 100, 290, LCD.BLUE)
        seconds -= 1
        utime.sleep_ms(900)
        
LCD = display.LCD_3inch5()
LCD.fill_rect(0, 0, LCD.width, LCD.height, LCD.YELLOW)
LCD.font = font
LCD.bl_ctrl(50)
LCD.text("Raspberry Pi Pico",170,17,LCD.BLUE)
connect()
clock()