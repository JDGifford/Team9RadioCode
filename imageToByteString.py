import datetime
import struct
#start = datetime.datetime.now()

def getImageData():
    ba = []

    with open("FilesToSend.zip", "rb") as image:
        im = image.read()
        ba = bytearray(im)

    sendArray = []

    for i in range(0, len(ba), 32):
        t = bytes(ba[i:min(i+32, len(ba))])
        sendArray.append(t)
        
    #end = datetime.datetime.now()
    #print(end-start)

    #print(len(sendArray))
    #sendArray.insert(0, len(sendArray).to_bytes(1, "little")) #adds the length of the array to the start of it
    return sendArray

    #for s in sendArray:
    #    print(len(s), end=" ")
