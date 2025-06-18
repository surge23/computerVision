import cv2
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import time

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
            hand_landmarks = result.multi_hand_landmarks[0]  
            thumb = hand_landmarks.landmark[4]                        
            index = hand_landmarks.landmark[8]       

            # height and width of the frame
            height = img.shape[0]
            width = img.shape[1]
            
            # converting x and y values into coordinates for line drawing
            thumb_x, index_x = int(thumb.x * width), int(index.x * width)
            thumb_y, index_y = int(thumb.y * height), int(index.y * height)

            distance = math.sqrt((thumb_x-index_x)**2 + (thumb_y-index_y)**2)
            # print(distance)
            vol = np.interp(distance, [15,250], [volumeMin, volumeMax])
            cv2.line(img, (thumb_x,thumb_y), (index_x,index_y), (0,255,255), 3)            
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            volume.SetMasterVolumeLevel(vol,None)
    cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break