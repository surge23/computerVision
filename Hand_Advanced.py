import cv2
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
# import time

mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumeMin, volumeMax, _ = volume.GetVolumeRange()

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()                                                                   #BGR
    new_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                                              #RGB conversion
    result = hand.process(new_img) 
    if result.multi_hand_landmarks:
        # for hand_landmarks in result.multi_hand_landmarks:
            # print(hand_landmarks)                                                             # Prints x,y,z coordinates of hands
            
            # variables for different landmarks
            hand_landmarks = result.multi_hand_landmarks[0]  
            thumb = hand_landmarks.landmark[4]                        
            index = hand_landmarks.landmark[8]      
            pinky = hand_landmarks.landmark[20]
            pinky1 = hand_landmarks.landmark[17]

            # height and width of the frame
            height = img.shape[0]
            width = img.shape[1]
            
            # converting x and y values into coordinates for line drawing
            thumb_x, index_x = int(thumb.x * width), int(index.x * width)
            thumb_y, index_y = int(thumb.y * height), int(index.y * height)
            pinky_x, pinky_y = int(pinky.x * width), int(pinky.y * height)
            pinky1_x, pinky1_y = int(pinky1.x * width), int(pinky1.y * height)

            # print(f"{pinky_x} and {pinky_y} : {pinky1_x} and {pinky_y}")

            distance = math.sqrt((thumb_x-index_x)**2 + (thumb_y-index_y)**2)
            # print(distance)
            # vol = np.interp(distance, [15,250], [volumeMin, volumeMax])
            vol = np.interp(distance, [15,250], [0, 100])
            Bar = np.interp(distance , [15,250], [400,100])                                      # for volume bar
            filter = 5
            vol = filter * round(vol/filter)


            cv2.line(img, (thumb_x,thumb_y), (index_x,index_y), (0,255,255), 3)                     # draws line between index and thumb
            cv2.rectangle(img, (50,100), (100,400), (255,255,0), 3)
            # cv2.rectangle(img, (50, int(volBar)), (100,400), (255,255,0), cv2.FILLED)                     
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)               # draws landmarks on hand when detected

            # volume.SetMasterVolumeLevel(vol,None)
            if pinky.x > pinky1.x:
                volume.SetMasterVolumeLevelScalar(vol/100,None)
                cv2.rectangle(img, (50, int(Bar)), (100,400), (255,255,0), cv2.FILLED)              # volume bar rectangle
                cv2.putText(img, f'Volume: {vol}', (40,450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 3)    
    
    cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break