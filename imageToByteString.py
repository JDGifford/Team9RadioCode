import datetime
start = datetime.datetime.now()

def getImageData():
    ba = []

    with open("deathstarredcircle.png", "rb") as image:
        im = image.read()
        ba = bytearray(im)

    sendArray = []

    for i in range(0, len(ba), 32):
        t = []
        for b in range(0, 32):
            if i+b < len(ba):
                t.append(ba[i+b])
        sendArray.append(t)
        
    end = datetime.datetime.now()
    print(end-start)
    return sendArray

    #for s in sendArray:
    #    print(len(s), end=" ")

    