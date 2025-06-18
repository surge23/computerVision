# Hand Gesture Volume Control
This project is a Gesture based volume control of your Windows PC. We use MediaPipe and openCV library to build this project.
A hand is detected using mediapipe library. Pycaw library is used to access volume control of your PC. This is specifically for windows since pycaw does not suppot linux or macOS. The code is pretty simple.
Hand.py is the general volume control using tip of thumb and index finger. Hand_advanced.py is where we smooth out the values and the volume is set at a desired level using pinky finger. 
This only detects one hand at a time. I prefer to use right hand and the logic is designed for right hand as well. When you use Hand_advanced.py, bring your hand closer to laptop camera and set the volume by decreasing or increasing the distace between index finger and thumb. The code will draw a line between these two points as well. When desired volume is reached, drop down the pinky finger to set it at the desired level. 
