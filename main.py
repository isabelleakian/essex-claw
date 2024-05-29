import cv2
import mediapipe as mp
import pyfirmata2
import time
import math

# pic = cv2.imread("knowledge questions.jpg")
# cv2.imshow("new-window", pic)
# cv2.imwrite("new-window.jpg", pic)
# cv2.waitKey()
# cv2.destroyAllWindows()

board = pyfirmata2.Arduino('COM11')
ledPin = board.get_pin('d:11:p')

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=1)


while True:
    # ledPin.write(0.5)
    success, frame = cap.read()
    if success:
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks:
            handLandmarks = result.multi_hand_landmarks[0]
            thumbTip = handLandmarks.landmark[4]
            indexTip = handLandmarks.landmark[8]
            # print(thumbTip)
            # print(indexTip)
            distance = math.sqrt((thumbTip.x - indexTip.x)**2 + (thumbTip.y - indexTip.y)**2)
            # print(distance)
            ledPin.write(distance)

            # for hand_landmarks in result.multi_hand_landmarks:
            #     print(hand_landmarks)
            mp_drawing.draw_landmarks(frame, handLandmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("capture image", frame)
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()
