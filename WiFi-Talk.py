from machine import Pin, SPI
import time
import ili9341 as module
import network
import espnow

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320

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

#self b'\x8c\x94\xdfN\x98\x84'
cams = [b'\x8c\x94\xdfNl\xc8', b'\x8c\x94\xdfO"\xc4']

peer = cams[0]
esp.add_peer(peer, channel=1)

esp.send(peer, "Hello from Main".encode("utf-8"))
time.sleep(2)
esp.send(peer, b'end')