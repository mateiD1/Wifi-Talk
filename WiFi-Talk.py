from machine import Pin, SPI
import time
import ili9341 as module
import xglcd_font as Font
import network
import espnow
import xpt2046

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320
FONT = Font.XglcdFont(path="fonts/EspressoDolce18x24.c", width=18, height=24)
COLOR = module.color565(255, 255, 255)

PIN_BL = Pin(21, Pin.OUT)
PIN_BL.value(1)

screen = SPI(1, baudrate=20000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = module.Display(screen, cs=Pin(15), dc=Pin(2), rst=Pin(17))

touch_screen = SPI(2, baudrate=1000000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))
touch = xpt2046.Touch(touch_screen, cs=Pin(33))

wifiRadio = network.WLAN(network.WLAN.IF_STA)
wifiRadio.active(True)
wifiRadio.disconnect()

esp = espnow.ESPNow()
esp.active(True)
esp.add_peer(b'\x8c\x94\xdfNl\xc8', channel=1)
esp.add_peer(b'\x8c\x94\xdfO"\xc4', channel=1)

class Text():
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

class Peer():
    def __init__(self, x, y, text, mac):
        self.x = x
        self.y = y
        self.text = text
        self.mac = mac

#self b'\x8c\x94\xdfN\x98\x84'
allPeers = [Peer(30, 36, "Cam-BUE", b'\x8c\x94\xdfNl\xc8'),
            Peer(30, 62, "Cam-BAL", b'\x8c\x94\xdfO"\xc4')]

allTexts = [Text(30, 114, "More left"),
            Text(30, 140, "More right"),
            Text(30, 162, "More up"),
            Text(30, 184, "More down"),
            Text(30, 210, "Zoom in"),
            Text(30, 232, "Zoom out"),
            Text(30, 258, "Prepare next"),
            Text(30, 284, "Live in 5s")]

def draw_setup():
    display.draw_text(x=10, y=10,
                text="Send to:",
                font=FONT,
                color=COLOR)

    display.draw_text(x=180, y=10,
                text="SEND",
                font=FONT,
                color=COLOR)
    
    for i in range(len(allPeers)):
        currPeer = allPeers[i]
        display.draw_text(x=currPeer.x, y=currPeer.y,
                text=currPeer.text,
                font=FONT,
                color=COLOR)
    
    display.draw_text(x=10, y=88,
                        text="Message:",
                        font=FONT,
                        color=COLOR)
    
    for i in range(len(allTexts)):
        currText = allTexts[i]
        display.draw_text(x=currText.x, y=currText.y,
                text=currText.text,
                font=FONT,
                color=COLOR)

def draw_text(info, color):
    display.draw_text(x=info.x, y=info.y,
                        text=info.text,
                        font=FONT,
                        color=color)

draw_setup()

curr_live = 0
prev_peer = 0
draw_text(allPeers[prev_peer], module.color565(0, 0, 255))
prev_mess = 0
draw_text(allTexts[prev_mess], module.color565(255, 0, 0))
while True:
    res = touch.raw_touch()
    if res != None:
        res_n = touch.normalize(res[0], res[1])
        x = 0 + res_n[0]
        y = 320 - res_n[1] # we have the charging port on top format
        
        # SEND x=180, y=10
        if x > 175 and y < 40:
            esp.send(allPeers[prev_peer].mac, (allTexts[prev_mess].text).encode("utf-8"))
            display.draw_text(x=180, y=10,
                        text="SEND",
                        font=FONT,
                        color=module.color565(0, 255, 0))
            
            if allTexts[prev_mess].text == "Live in 5s" and curr_live != prev_peer:
                other_peer_ind = 0
                if prev_peer == 0:
                    other_peer_ind = 1 
                esp.send(allPeers[other_peer_ind].mac, ("Toggle Live").encode("utf-8"))
                curr_live = prev_peer
            
            time.sleep(0.5)
            display.draw_text(x=180, y=10,
                        text="SEND",
                        font=FONT,
                        color=COLOR)
            continue
        
        if y > 95:
            ind_mess = min(range(len(allTexts)), key=lambda i: abs(y - allTexts[i].y - 24))
            message = allTexts[ind_mess].text
            # selection
            draw_text(allTexts[ind_mess], module.color565(255, 0, 0))
            if prev_mess != ind_mess:
                draw_text(allTexts[prev_mess], module.color565(255, 255, 255))
                prev_mess = ind_mess
        else:
            ind_peer = min(range(len(allPeers)), key=lambda i: abs(y - allPeers[i].y - 24))
            peer = allPeers[ind_peer].mac
            # selection
            draw_text(allPeers[ind_peer], module.color565(0, 0, 255))
            if prev_peer != ind_peer:
                draw_text(allPeers[prev_peer], module.color565(255, 255, 255))
                prev_peer = ind_peer
