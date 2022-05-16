import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import time
import datetime

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1) # max faces for detection is 1
plotY = LivePlot(640,360,[10,40], invert=True)

blinkCounter = 0
counter = 0

idList = [133,155,154,153,145,144,163,7,33,246,161,160,159,158,157,173,
          362,398,384,385,386,387,388,466,263,249,390,373,374,380,381,382]
ratioList = []

l_p = time.time()
last = 0
time.sleep(1)
print("Time                      ", "Blink Count")

while True:


    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT): # to run the video file infinite times
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)



    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0] # the only face we have
        for id in idList:
            cv2.circle(img, face[id], 3, (255, 0, 0), cv2.FILLED)

        leftUp = face[159]
        leftDown = face[145]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVer,_ = detector.findDistance(leftUp, leftDown)
        lengthHor,_ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, (0,200,0), 2)
        cv2.line(img, leftLeft, leftRight, (0,200,0), 2)


        ratio = int((lengthVer/lengthHor)*100)
        ratioList.append(ratio)
        if len(ratioList) > 4:
            ratioList.pop(0)
        ratioAvg = sum(ratioList)/len(ratioList)


        if ratioAvg < 23 and counter == 0:
            blinkCounter += 1
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0

        cvzone.putTextRect(img, f'Blinks : {blinkCounter}', (50,100), 2, 2, (255,255,255),(0,255,0) )
        cvzone.putTextRect(img,f'{last}',(100,50))
        imgPlot = plotY.update(ratioAvg)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot],2,1)


    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)


    cv2.imshow("Image", imgStack)
    cv2.waitKey(1)
    if time.time() - l_p >= 5:
        last = blinkCounter
        print(datetime.datetime.now(), blinkCounter)
        l_p = time.time()
        blinkCounter = 0

