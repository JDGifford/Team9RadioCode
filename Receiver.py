# Receiving module code

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

address = [b"1node", b"2node"]

output = []

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.set_pa_level(RF24_PA_LOW) # Set to low power for close range testing

# Set addresses for transmission and receiving
radio.open_tx_pipe(address[1])
radio.open_rx_pipe(1, address[0])

radio.dynamic_payloads = True

radio.listen = True
count = 0
length = 0

if radio.available(): # Gets the number of payloads expected to be received
    length = radio.get_dynamic_payload_size()
    imageSize = radio.read(struct.unpack("<I", length)[0])

#try:
#    while (True):
#        if radio.available():
#            length = radio.get_dynamic_payload_size()
#            payload = radio.read(length)
#            output.append(payload)
#            print("Recieved Payload: " + str(payload))
#            count += 1
#except (KeyboardInterrupt): #Testing to see if we can get the file and just manually ending when it's all received
#    oFile = open("outputZip.zip", "wb")
#    for l in output:
#        oFile.write(l)
#    oFile.close()
#    radio.listen = False

while (count < length):
        if radio.available():
            length = radio.get_dynamic_payload_size()
            payload = radio.read(length)
            output.append(payload)
            print("Recieved Payload: " + str(payload))
            count += 1    

oFile = open("outputZip.zip", "wb")
for l in output:
    oFile.write(l)
    oFile.close()
    radio.listen = False