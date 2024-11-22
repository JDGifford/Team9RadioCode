# Transmission module code
# This code will convert an input into bytes and send it to the
# receiving module

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

payload = getImageData() # store the payloads to send

temp = bytearray()
for t in bytearray:
    temp.extend(t)

payloadMD5 = hashlib.md5(temp).digest
print(len(payloadMD5))

temp = 0 #just so we're not storing something so huge in memory the whole time

address = [b"1node", b"2node"]

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.set_pa_level(RF24_PA_LOW) # Set to low power for close range testing
radio.setDataRate(RF24_2MBPS)

# Set addresses for transmission and receiving
radio.open_tx_pipe(address[0])
radio.open_rx_pipe(1, address[1])

radio.dynamic_payloads = True
radio.ack_payloads = True

arraySize = len(payload)
radio.listen = False

start = time.monotonic()
#print("Sending array size..." + str(arraySize))
#sent = False
#while (not sent):
#    if (radio.write(struct.pack("L", arraySize))): # send the number of packets in the image first
#        sent = True
#        print("Array Size sending successful.")
#    else:
#        radio.reuse_tx()

radio.flush_tx()
iterator = 0
failures = 0
for pack in payload:
    print("Sending packet " + str(iterator) + "...")
    packetSent = False
    while (not packetSent):
        if radio.write(pack):
            packetSent = True
            if (radio.available()):
                result = radio.read(radio.get_dynamic_payload_size())
                rCount = struct.unpack("L", result)[0]
                # Abandoned branch, I was using acknowledgement payloads to try to match iterators, wasn't as useful as I had hoped
                # Honestly I think this setup is successful error-checking enough for now?
                # The two generals problem points to "good enough" being the best we can do
        else:
            failures += 1
            radio.reuse_tx()
            if failures > 99 and iterator < 7:
                iterator = arraySize + 1
                print("Make sure receiver is listening. Exiting sending program")
                radio.flush_tx()
                break   
    iterator += 1

print("Sending MD5 sum...")
sent = False
while (not sent):
    if (radio.write(payloadMD5)): # send the number of packets in the image first
        sent = True
        print("MD5 sum sending successful.")
    else:
        radio.reuse_tx()

end = time.monotonic()
print (end-start)