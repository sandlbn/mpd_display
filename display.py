from LCD import LCD
from mpd import MPDClient
import time
import random

lcd = LCD() # params available for rPi revision, I2C Address, and backlight on/off
            # lcd = LCD(2, 0x3F, True)

client = MPDClient()
client.connect("localhost", 6600)

def parse_audio(audio):
    d = audio.split(":")
    if len(d) == 3:
        return "{0}/{1}".format(float(int(d[0])/100)/10, d[1])
    elif len(d) == 2:
        return "{0}/{1}".format(d[0], d[1])
    else:

        return ""
def current_song(current):
    try:
        return (current['artist'], current['title'])
    except KeyError:
        return (current['name'], current['title'])

def show_time(st):
   
    elapsed_m, elapsed_s = divmod(float(st['elapsed']),60)
    try:
        duration_m, duration_s = divmod(float(st['duration']),60)
        print_time = "{:02d}:{:02d}/{:02d}:{:02d}".format(int(elapsed_m), int(elapsed_s),int(duration_m), int(duration_s))
    except KeyError:
        print_time = "{:02d}:{:02d}".format(int(elapsed_m), int(elapsed_s))

    return print_time

while True:
    time.sleep(1)
    st =  client.status()
    print st
    current = client.currentsong()
    if st["state"] == "play":
        try:
            line = "{0} v {1}% {2}".format(st["state"],st["volume"], parse_audio(st['audio'])) 
            lcd.message(line ,1)
            lcd.message("{0}".format(show_time(st)),2)
            lcd.message(current_song(current)[0],3)
            lcd.message(current_song(current)[1],4)
        except KeyError:
            pass
    else:

        lcd.lcd_byte_dark(0x0C, 0)
    
#lcd.clear() # clear LCD display

