#STARTERHACKS 2019
#BY: Aswin, Sultan, Anand, Kokelan and Tyler

#Imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import RPi.GPIO as GPIO

#Setting up buzzer
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Set buzzer - pin 21 as output
buzzer=21 
GPIO.setup(buzzer,GPIO.OUT)

#Setting up camera
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(320, 240))

display_window = cv2.namedWindow("QuickSense")

car_cascade = cv2.CascadeClassifier('lbpcascade_silverware.xml')

time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array

    #Object Detection
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    GPIO.output(buzzer,GPIO.LOW) #When object is not detected, set buzzer state to "low"
    for (x,y,w,h) in cars:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        GPIO.output(buzzer,GPIO.HIGH) #When object is detected, set buzzer state to "high"
        
    
    
    #Displays Output to Window
    cv2.imshow("QuickSense", image)
    key = cv2.waitKey(1)

    rawCapture.truncate(0)

    if key == 27:
        camera.close()
        cv2.destroyAllWindows()
        break
