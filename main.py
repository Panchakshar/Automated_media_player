import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pTime=0
cTime=0

while True:
  success,img = cap.read()
  img = cv.flip(img, 1)
  imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
  #Processing the CAptured Image
  results = hands.process(imgRGB)
  #print(results.multi_hand_landmarks)
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      for id,lm in enumerate(hand_landmarks.landmark):
        #coordinates in decimal
        #print(id,lm)
        #coordiantes in pixel
        h,w,c = img.shape
        cx, cy = int(lm.x*w),int(lm.y*h)
        print(id,cx,cy)
        #Working on indvidual points
        if id==12:
          cv.circle(img,(cx,cy),15,(255,0,255),cv.FILLED)


      #Drawing the points and connections
      mp_drawing.draw_landmarks(
        img,
        hand_landmarks,
        mphands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())

  #calculating fps
  cTime = time.time()
  fps = 1/(cTime-pTime)
  pTime = cTime

  #Printing the fps on the screen
  cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
  #Showing the image
  cv.imshow("Image",img)
  #Wating for the escape key
  if cv.waitKey(1) == 27:
    cv.destroyAllWindows()
    cap.release()
    break
