# Transmission module code
# This code will convert an input into bytes and send it to the
# receiving module

import time
import struct
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER
from imageToByteString import getImageData

CSN_PIN = 0
if RF24_DRIVER == "MRAA":
    CE_PIN = 15
elif RF24_DRIVER == "wiringPi":
    CE_PIN = 3
else:
    CE_PIN = 22

radio = RF24(CE_PIN, CSN_PIN)

payload = getImageData() # store the payloads to send

address = [b"1node", b"2node"]

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.set_pa_level(RF24_PA_LOW) # Set to low power for close range testing

# Set addresses for transmission and receiving
radio.open_tx_pipe(address[0])
radio.open_rx_pipe(1, address[1])

radio.dynamic_payloads = True

arraySize = len(payload)

radio.listen = False
for c in range(arraySize):
    
    radio.flush_tx()
    iterator = 0
    failures = 0
    while iterator < arraySize:
        if not radio.write_fast(payload[iterator]):
            failures += 1
            radio.reuse_tx()
            if failures > 99 and iterator < 7 and c < 2:
                iterator = arraySize + 1
                print("Make sure receiver is listening. Exiting sending program")
                radio.flush_tx()
                break
            iterator += 1