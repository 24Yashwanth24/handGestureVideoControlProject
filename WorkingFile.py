import HandTrackingModule as htm
import numpy as np
import time
import cv2
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import (AudioUtilities, IAudioEndpointVolume)
import pyautogui


################################
wCam, hCam = 2020,1080
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector()



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
 #volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]



while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img= (detector.findHands(img))
    lmList, bbox = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        #print(lmList[4], lmList[8])


        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[16][1], lmList[16][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2


        cv2.circle(img,(x1,y1),15,(255,0,255), cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255), cv2.FILLED)
        cv2.circle(img,(x3,y3),15,(0,0,255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        cv2.line(img, (x1, y1), (x3, y3), (0, 0, 0), 2)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        lengthvol = math.hypot(x2-x1,y2-y1)
        lengthpl = math.hypot(x3-x1,y3-y1)

        #print(length)
        #hand rate 50 - 300
        # volume rate  65 - 0

        vol = np.interp(lengthvol, (50,300), (minVol, maxVol))
        #print(int(lengthvol), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if lengthpl < 50:
            cv2.circle(img,(cx,cy),15,(0,0,255),cv2.FILLED)
            pyautogui.press('space')



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}',(40,70), cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),2)

    cv2.imshow('Img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

