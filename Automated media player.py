import cv2 as cv
import mediapipe as mp
import HandTrackingModule as ht
import time
import pyautogui


def count_fingers(lst):
  cnt = 0

  thresh = (lst[9][2] - lst[0][2]) / 2

  if (lst[5][2] - lst[8][2]) > thresh:
    cnt += 1

  if (lst[9][2] - lst[12][2]) > thresh:
    cnt += 1

  if (lst[13][2] - lst[16][2]) > thresh:
    cnt += 1

  if (lst[17][2] - lst[20][2]) > thresh:
    cnt += 1

  if (lst[5][1] - lst[4][1]) > 6:
    cnt += 1

  return cnt

pTime = 0
cTime = 0
cap = cv.VideoCapture(0)
detector = ht.handDetector(maxHands=1)

start_init = False

prev = -1

while True:
  end_time = time.time()
  success, img = cap.read()
  img = cv.flip(img,1)
  image = detector.findHands(img)
  List = detector.findPosition(image)
  if len(List) != 0:
    cnt = count_fingers(List)

  if not (prev == cnt):
    if not (start_init):
      start_time = time.time()
      start_init = True

    elif (end_time - start_time) > 0.2:
      if (cnt == 1):
        pyautogui.press("right")

      elif (cnt == 2):
        pyautogui.press("left")

      elif (cnt == 3):
        pyautogui.press("up")

      elif (cnt == 4):
        pyautogui.press("down")

      elif (cnt == 5):
        pyautogui.press("space")

      prev = cnt
      start_init = False

  cTime = time.time()
  fps = 1 / (cTime - pTime)
  pTime = cTime

  cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
  cv.imshow("Image", img)
  if  cv.waitKey(1)==27:
    cv.destroyAllWindows()
    cap.release()
    break