# Receiving module code

import time
import struct
import hashlib
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER, RF24_2MBPS
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
radio.setDataRate(RF24_2MBPS)

# Set addresses for transmission and receiving
radio.open_tx_pipe(address[1])
radio.open_rx_pipe(1, address[0])

radio.dynamic_payloads = True
radio.ack_payloads = True

radio.listen = True
count = 0
imageSize = 0

#while (imageSize == 0):
#    if radio.available(): # Gets the number of payloads expected to be received
#        length = radio.get_dynamic_payload_size()
#        payload = radio.read(length)
#        imageSize = struct.unpack("L", payload)[0]
#        print(imageSize)

radio.write_ack_payload(1, struct.pack("L", count))        

finished = False
while (not finished):
        if radio.available():
            length = radio.get_dynamic_payload_size()
            payload = radio.read(length)
            output.append(payload)
            print("Recieved Payload: " + str(count))
            count += 1
            radio.write_ack_payload(1, struct.pack("L", count))
            if (length < 32):
                finished = True

outputMD5 = hashlib.md5(output).digest()

getmd5 = False
md5Result = 0

while (not getmd5):
    if radio.available():
        length = radio.get_dynamic_payload_size()
        md5Result = radio.read(length)
        if (outputMD5 == md5Result):
            print("MD5 sums match!")
        else:
            print("MD5 sum mismatch.")
        

oFile = open("outputZip.zip", "wb")
for l in output:
    oFile.write(l)
    
oFile.close()
print("Transmission complete.")
radio.listen = False