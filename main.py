import cv2
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector

def close_window(camera):
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        camera.release()
        cv2.destroyAllWindows()
        exit()

camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)

detector = HandDetector(detectionCon=0.3, maxHands=1)

screen_width, screen_height = pyautogui.size() 

def program_utama():
    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            print("Failed to open the camera")
            break
        frame = cv2.flip(frame, 1)

        hands, gambar = detector.findHands(frame)
        if hands:
            hand = hands[0]
            lmList = hand["lmList"]
            if len(lmList) != 0:
                fingers = detector.fingersUp(hand)
                x1, y1 = lmList[8][0], lmList[8][1]
                x5, y5 = lmList[20][0], lmList[20][1]

                h, w, _ = frame.shape
                x1 = np.interp(x1, (0, w), (0, screen_width))
                y1 = np.interp(y1, (0, h), (0, screen_height))

                if sum(fingers) == 0:
                    pass
                elif fingers[1] == 1 and sum(fingers) == 1:
                    pyautogui.moveTo(x1, y1)
                elif fingers[1] == 1 and fingers[2] == 1 and sum(fingers) == 2:
                    pyautogui.click(button='left')
                    cv2.putText(gambar, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif fingers[1] == 1 and fingers[4] == 1 and sum(fingers) == 2:
                    pyautogui.click(button='right')
                    cv2.putText(gambar, "Right Click", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Handy Cursor", gambar)
        close_window(camera)

if __name__ == "__main__":
    program_utama()