import cv2
import mediapipe as mp
import pyautogui
import pygetwindow as gw
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Screen size
screen_width, screen_height = pyautogui.size()

# Gesture state for right-click
right_click_timer = 0
right_click_done = False

def get_active_platform():
    window_title = gw.getActiveWindowTitle() or ""
    if "YouTube" in window_title:
        return "youtube"
    return "other"

def get_finger_status(hand_landmarks):
    tips = [mp_hands.HandLandmark.THUMB_TIP,
            mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            mp_hands.HandLandmark.RING_FINGER_TIP,
            mp_hands.HandLandmark.PINKY_TIP]
    pip_joints = [mp_hands.HandLandmark.THUMB_IP,
                  mp_hands.HandLandmark.INDEX_FINGER_PIP,
                  mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                  mp_hands.HandLandmark.RING_FINGER_PIP,
                  mp_hands.HandLandmark.PINKY_PIP]
    
    return [hand_landmarks.landmark[t].y < hand_landmarks.landmark[p].y for t, p in zip(tips, pip_joints)]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            platform = get_active_platform()
            finger_open = get_finger_status(hand_landmarks)
            thumb_open, index_open, middle_open, ring_open, pinky_open = finger_open

            # Coordinates for fingers
            index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert to screen coordinates
            cursor_x = int(index.x * screen_width)
            cursor_y = int(index.y * screen_height)
            pyautogui.moveTo(cursor_x, cursor_y, duration=0.01)

            # ----------- GESTURES -----------

            # YouTube Control Gestures
            if platform == "youtube":
                if index_open and not any([middle_open, ring_open, pinky_open, thumb_open]):
                    print("➡️ Next Reel")
                    pyautogui.press('down')

                elif index_open and middle_open and not any([ring_open, pinky_open, thumb_open]):
                    print("⬅️ Previous Reel")
                    pyautogui.press('up')

                elif all(finger_open):
                    print("▶️ Resume")
                    pyautogui.press('space')

                elif not any(finger_open):
                    print("⏸️ Pause")
                    pyautogui.press('space')

                elif thumb_open and not any([index_open, middle_open, ring_open, pinky_open]) and thumb.x < 0.2:
                    print("⬅️ Back Page")
                    pyautogui.hotkey('alt', 'left')

                elif pinky_open and not any([index_open, middle_open, ring_open, thumb_open]) and pinky_open and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x + 0.1:
                    print("➡️ Forward Page")
                    pyautogui.hotkey('alt', 'right')

                elif index_open and not thumb_open and index.y < 0.4:
                    print("⬆️ Scroll Up")
                    pyautogui.scroll(20)

                elif index_open and thumb_open and abs(index.x - thumb.x) > 0.15:
                    print("⬇️ Scroll Down")
                    pyautogui.scroll(-20)

                elif index_open and thumb_open and abs(index.x - thumb.x) < 0.05 and abs(index.y - thumb.y) < 0.05:
                    print("🔘 Select/Pause")
                    pyautogui.click()
                    time.sleep(0.5)

            # Universal mouse click (when not YouTube or always active)
            # Pinch (index + thumb) → Left Click
            if index_open and thumb_open and abs(index.x - thumb.x) < 0.05 and abs(index.y - thumb.y) < 0.05:
                if not right_click_done:
                    print("🖱️ Left Click")
                    pyautogui.click()
                    time.sleep(0.3)
                    right_click_done = True
            else:
                right_click_done = False

            # Right Click → Hold pinch for >1 sec
            if index_open and thumb_open and abs(index.x - thumb.x) < 0.05 and abs(index.y - thumb.y) < 0.05:
                if right_click_timer == 0:
                    right_click_timer = time.time()
                elif time.time() - right_click_timer > 1.2:
                    print("🖱️ Right Click")
                    pyautogui.click(button='right')
                    time.sleep(0.5)
                    right_click_timer = 0
            else:
                right_click_timer = 0

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture + Virtual Mouse (Right Hand)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
