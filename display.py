from LCD import LCD
from mpd import MPDClient
import time
import random

DISP_LEN = 20
lcd = LCD()  # params available for rPi revision, I2C Address, and backlight on/off
# lcd = LCD(2, 0x3F, True)

client = MPDClient()
client.connect("localhost", 6600)


def display_long_text(from_ch, txt):
    return txt[from_ch:]


def display_text(txt, prev_pos=0):
    if len(txt) > DISP_LEN:
        if prev_pos == 0:
            return display_long_text(prev_pos, txt), prev_pos+1
        elif DISP_LEN-1 == (len(txt)-prev_pos):
            return display_long_text(prev_pos, txt), 0
        else:
            return display_long_text(prev_pos, txt), prev_pos+1
    else:
        return txt, 0


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

    elapsed_m, elapsed_s = divmod(float(st['elapsed']), 60)
    try:
        duration_m, duration_s = divmod(float(st['duration']), 60)
        print_time = "{:02d}:{:02d}/{:02d}:{:02d}".format(
            int(elapsed_m), int(elapsed_s), int(duration_m), int(duration_s))
    except KeyError:
        print_time = "{:02d}:{:02d}".format(int(elapsed_m), int(elapsed_s))

    return print_time


cur_song = ""
cur_art = ""
cur_song_idx = 0
cur_art_idx = 0

while True:
    time.sleep(0.2)
    st = client.status()
    current = client.currentsong()
    if st["state"] == "play":
        try:
            line = "{0} v {1}% {2}".format(
                st["state"], st["volume"], parse_audio(st['audio']))
            lcd.message(line, 1)
            lcd.message("{0}".format(show_time(st)), 2)
            if cur_art != current_song(current)[1]:
                cur_art_idx = 0
                cur_song_idx = 0
            cur_song = current_song(current)[0]
            cur_art = current_song(current)[1]
            disp_song, song_new_idx = display_text(cur_song, cur_song_idx)
            disp_art, art_new_idx = display_text(cur_art, cur_art_idx)
            cur_song_idx = song_new_idx
            cur_art_idx = art_new_idx
            lcd.message(disp_song, 3)
            lcd.message(disp_art, 4)
        except KeyError:
            pass
    else:

        lcd.lcd_byte_dark(0x0C, 0)

# lcd.clear() # clear LCD display
