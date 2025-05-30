import math
import cv2
import numpy as np
import pygame
import time
import serial

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #pre-trained face detection model

cap = cv2.VideoCapture(0) #connect to the webcam (0 for laptop default, 1 for external; make sure it is not being used somewhere else)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

max_angel = math.radians(78) #horizontal camera angel (from camera description)
servo_center = 90 #max angle of servo motor (0-180 degrees)
flip_parameter = None #set acording to camera parametrs

center_screen_x = frame_width//2
center_screen_y = frame_height//2

cross_size = 10

red = (0, 0, 255)
yellow = (0, 200, 200)
white = (255, 255, 255)

pygame.mixer.init()

shoot_sound = pygame.mixer.Sound("shoot.mp3")

try:
    ser = serial.Serial('com3', 9600, timeout=0.1) 
    time.sleep(2)
except Exception as e:
    print("Serial connection failed: ", e)
    exit()

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

def draw_centre_cross(frame):
    cv2.line(frame, (center_screen_x - cross_size, center_screen_y), (center_screen_x + cross_size, center_screen_y), white, 2)
    cv2.line(frame, (center_screen_x, center_screen_y - cross_size), (center_screen_x, center_screen_y + cross_size), white, 2)

def aim_at_center(center_x, center_y):
    if abs(center_x - center_screen_x) < 10 and abs(center_y - center_screen_y) < 10:
        return True
    else:
        return False

def calc_alpha(x_difference, max_angel):
    h = (frame_width / 2) * math.tan(math.pi/2 - (max_angel/2))
    tan_alpha = x_difference/h
    alpha = math.atan(tan_alpha)
    #servo_angle = servo_center - math.degrees(alpha)
    #servo_angle = max(0, min(180, servo_angle))
    return alpha

def arduino_move(alpha):

    #code
    
    print("move: ", math.degrees(alpha))

def arduino_shoot():

    #code

    print("shoot!")
    shoot_sound.play()
    time.sleep(3)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    
    if flip_parameter:
        frame = cv2.flip(frame, -1) 
    
    draw_centre_cross(frame)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces: #for every face draw rectangles and crosses
        string = 'X{0:d}Y{1:d}'.format((x+w//2), (y+h//2))
        print(string)
        ser.write(string.encode('utf-8'))
        cv2.rectangle(frame, (x+w, y), (x+w+w, frame_height), (255, 255, 255), 2)
        
        #center of rectangle
        center_x = x + w // 2
        center_y = y + h // 2

        if aim_at_center(center_x, center_y):
            cv2.line(frame, (center_x - cross_size, center_y), (center_x + cross_size, center_y), red, 2)
            cv2.line(frame, (center_x, center_y - cross_size), (center_x, center_y + cross_size), red, 2)
            arduino_shoot()

        else:
            cv2.line(frame, (center_x - cross_size, center_y), (center_x + cross_size, center_y), yellow, 2)
            cv2.line(frame, (center_x, center_y - cross_size), (center_x, center_y + cross_size), yellow, 2)
            x_difference = center_x - center_screen_x
            arduino_move(calc_alpha(x_difference, max_angel))

    cv2.imshow('Webcam Face Detection', frame) #displaying frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release resources
cap.release()
cv2.destroyAllWindows()