#IMPORTANT# 
#before running, ensure that all the required libraries, packages and modules are installed or programme will not run

import cv2 
from deepface import DeepFace
import csv
import os
import time 

face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
camera= cv2.VideoCapture(0)



#previous_frame = 0
#new_frame = 0

#input("Before we begin how you feel right now?")
frame_count = 0 #the amount of frames set to 0

analysis_frequency = 10 #sets the analysis frequency (I had a problem where it was really laggy due to low fps)

possible_emotions = ['angry', 'disgust','fear','happy','sad','surprise', 'neutral']
emo_counter = {emotion: 0 for emotion in possible_emotions}
emo_start_time = {emotion: time.time() for emotion in possible_emotions}
emo_duration = {emotion: 0 for emotion in possible_emotions}
new_file = "my_file.csv"
emotion = ''
last_emo = None






if os.path.exists(new_file):#deletes previous file
    os.remove(new_file)

while camera.isOpened(): #---->checks whether or not camera is opened
    _,frame = camera.read()
    font = cv2.FONT_HERSHEY_PLAIN
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#changes image to greyscale image to make sure the picture is good                                           
    person=face.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    #previous_frame = 0
    #new_frame = time.time()
    #fps = 1/(new_frame-previous_frame) 
    #previous_frame=new_frame
    #fps = int(fps)
    #fps = str(fps)
    #cv2.putText(frame, fps, (165,40), font, 2,(6,159,189),1, cv2.LINE_AA)#shows fps on the open window
    emotion_data = ['' for _ in range(len(possible_emotions))]
    if len(person) == 0: # ----->>if no face is detected
        cv2.putText(frame, "No Face", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
    else:
        for x,y,w,h in person: #----> x,y= front of face left and right then w,h = top and bottom of face
            cv2.rectangle(frame, (x,y), (x+w,y+h), (127,255,0),1 )

            if frame_count % analysis_frequency == 0: #slows down analysis frequency
                analyze = DeepFace.analyze(frame, enforce_detection=False, actions=["emotion"])
                emotion = analyze["dominant_emotion"]
                emo_counter[emotion]+=1
                if emotion != last_emo:
                    if last_emo is not None:
                        emo_duration[last_emo]+=time.time() -emo_start_time[last_emo]
                    emo_start_time[emotion]=time.time()
                    last_emo = emotion
            
                print(emotion)

        cv2.putText(frame, emotion,(x, y-10), font, 1,(0,255,0),2)
    
    frame_count += 1               
    cv2.imshow("camera" , frame)
    key=cv2.waitKey(1)
    if key==ord("w"): #press w to break out of camera
        break
    elif key==ord('W'):
        break

# database
with open(new_file, 'a', newline='') as file:
    db = csv.writer(file)
    db.writerow(['Emotion', 'Count', 'Duration(s)'])
    for emotion in possible_emotions:
         db.writerow([emotion, emo_counter[emotion], emo_duration[emotion]])

camera.release()
cv2.destroyAllWindows()