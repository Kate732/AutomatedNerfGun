import math
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #pre-trained face detection model

cap = cv2.VideoCapture(2) #connect to the webcam (0 for laptop default, 1 for external; make sure it is not being used somewhere else)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

max_angel = math.radians(78) #horizontal camera angel (from camera description)
flip_parameter = None #set acording to camera parametrs

center_screen_x = frame_width//2
center_screen_y = frame_height//2

cross_size = 10

red = (0, 0, 255)
yellow = (0, 200, 200)
white = (255, 255, 255)

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
    return alpha

def arduino_move(alpha):

    #code
    
    print("move: ", math.degrees(alpha))

def arduino_shoot():

    #code

    print("shoot!")

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
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
        
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