from machine import Pin, SPI
import time
import ili9341 as module
import xglcd_font as Font
import network
import espnow

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320
FONT = Font.XglcdFont(path="fonts/ArcadePix9x11.c", width=9, height=11)
COLOR = module.color565(255, 0, 0)

PIN_RST = Pin(17)
PIN_CS = Pin(15)
PIN_DC = Pin(2)
PIN_SCLK = Pin(14)
PIN_MOSI = Pin(13)
PIN_MISO = Pin(12)
PIN_BL = Pin(21, Pin.OUT)
PIN_BL.value(1)

spi = SPI(1, baudrate=20000000, sck=PIN_SCLK, mosi=PIN_MOSI, miso=PIN_MISO)
display = module.Display(spi, cs=PIN_CS, dc=PIN_DC, rst=PIN_RST)

wifiRadio = network.WLAN(network.WLAN.IF_STA)
wifiRadio.active(True)
wifiRadio.disconnect()

esp = espnow.ESPNow()
esp.active(True)

def draw_message(msg):
    msg = msg.decode("utf-8")
    display.draw_text(x=50, y=50,
                text=msg,
                font=FONT,
                color=COLOR)

while True:
    host, msg = esp.recv()
    if msg:
        if msg == b'end':
            break
        draw_message(msg)