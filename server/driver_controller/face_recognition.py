import cv2
import time
import mmap
import numpy as np
from datetime import date

filepath='/home/pi/Desktop/server/variables.txt'

file_object=open(filepath,mode="r+",encoding="utf8")
mmap_object=mmap.mmap(file_object.fileno(),0,access=mmap.ACCESS_WRITE,offset=0)


recognizer = cv2.face_LBPHFaceRecognizer.create()

# Load the trained mode
recognizer.read('trainer/trainer.yml')

# Load prebuilt model for Frontal Face
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize and start the video frame capture
cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,720)

check_face=0
check_face_unknown=0
while True:
# Loop
    while True:
        if(mmap_object[80:81].decode()=='0' or mmap_object[80:81].decode()=='2'):
            while True:
                time.sleep(1)
                print("idle")
                if(mmap_object[80:81].decode()=='1'):break
        
        time.sleep(0.1)
        # Read the video frame
        ret, im =cam.read()

        # Convert the captured frame into grayscale
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        # Get all face from the video frame
        faces = faceCascade.detectMultiScale(gray, 1.2,5)

        # For each face in faces
        for(x,y,w,h) in faces:

            # Create rectangle around the face
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (255,255,0), 4)

            # Recognize the face belongs to which ID
            Id,confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
           #if(confidence<100):
                

            # Check the ID if exist
            if(Id==1):
                Id = "Enver"
                check_face=check_face+1
            elif(Id==2):
                Id = "Cagin"
                check_face=check_face+1
            else:
                Id = "Unknown"
                check_face_unknown=check_face_unknown+1
                

            # Put text describe who is in the picture
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
            cv2.putText(im, str(Id), (x,y-40), font, 2, (255,255,255), 3)

        # Display the video frame with the bounded rectangle
        cv2.imshow('im',im) 

        # If 'q' is pressed, close program
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        if(check_face==3):
            middle_image=im
        if(check_face==5):
            today=date.today()
            today=today.strftime("%d:%m:%y")
            mmap_object.seek(60)
            mmap_object.write(bytes(str(today),encoding="utf8"))
            mmap_object.write(bytes(str(':'),encoding="utf8"))
            
            instant_time = mmap_object[0:8].decode()
            mmap_object.write(bytes(str(instant_time),encoding="utf8"))
            
            path='face_recognation_photo_base/'+mmap_object[85:95].decode()+'/'+mmap_object[60:77].decode()+'.jpg'
            print(path)
            cv2.imwrite(path,middle_image)
            
            mmap_object.seek(80)
            mmap_object.write(bytes(str(2),encoding="utf8"))
            break
        
        if (check_face_unknown==20):
            mmap_object.seek(79)
            mmap_object.write(bytes(str(1),encoding="utf8"))
            mmap_object.write(bytes(str(0),encoding="utf8"))
            break

# Stop the camera
cam.release()

# Close all windows
cv2.destroyAllWindows()
