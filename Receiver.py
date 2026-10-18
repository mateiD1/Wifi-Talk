from machine import Pin, SPI
import ili9341 as module
import xglcd_font as Font
import network
import espnow
import time

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320
FONT = Font.XglcdFont(path="fonts/EspressoDolce18x24.c", width=18, height=24)
COLOR = module.color565(255, 255, 255)

screen = SPI(1, baudrate=20000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = module.Display(screen, cs=Pin(15), dc=Pin(2), rst=Pin(17))

wifiRadio = network.WLAN(network.WLAN.IF_STA)
wifiRadio.active(True)
wifiRadio.disconnect()

esp = espnow.ESPNow()
esp.active(True)

def draw_setup():
    display.draw_line(0, 50, 239, 50, COLOR)
    if not curr_live:
        go_off()
    else:
        go_live()

def go_live():
    display.fill_rectangle(0, 0, 240, 50, module.color565(255, 0, 0))
    global curr_live
    curr_live = True
    
def go_off():
    display.fill_rectangle(0, 0, 240, 50, module.color565(0, 255, 0))
    global curr_live
    curr_live = False
    
def get_time():
    hour = time.localtime()[3]
    min = time.localtime()[4]
    return f"{hour}:{min}"

y = 70
def draw_message(msg):
    display.draw_text(x=10, y=y,
                text=get_time()+": "+msg,
                font=FONT,
                color=COLOR)

curr_live = False
draw_setup()
draw_message("Starting...")
y += 26

while True:
    if y + 26 > 330:
        print(y)
        display.clear()
        draw_setup()
        y = 70
    
    host, msg = esp.recv()
    if msg:
        msg = msg.decode("utf-8")
        
        if msg == "Live in 5s":
            go_live()
        elif msg == "Toggle Live":
            go_off()
            continue
        
        draw_message(msg)
        y += 26