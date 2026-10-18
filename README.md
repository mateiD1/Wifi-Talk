# Wifi-Talk

Three ESP32 boards that communicate with each other. One master board sends messages to the other two, which show them on a display.

## How it works

- The master board sends messages to the two other boards.
- The receiving boards show each message with a timestamp on the display.
- A status bar on the display shows the state: red = live, green = off.

## Setup
