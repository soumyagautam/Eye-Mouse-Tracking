import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

reading_mode = False


def on_mouse_click(event, x, y, flags, param):
    global reading_mode

    if event == cv2.EVENT_LBUTTONDOWN:
        if button_top_left[0] <= x <= button_bottom_right[0] and button_top_left[1] <= y <= button_bottom_right[1]:
            if reading_mode:
                reading_mode = False
                print("Reading Mode Terminated!")
            else:
                reading_mode = True
                print("Reading Mode Activated!")


button_top_left = (1103, 25)  # Top-right corner
button_bottom_right = (1255, 65)

cv2.namedWindow("Sign Bridge: WL")
cv2.setMouseCallback("Sign Bridge: WL", on_mouse_click)

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)

    cv2.rectangle(frame, button_top_left, button_bottom_right, (0, 255, 0), -1)
    button_text = "Reading Mode"
    text_size = cv2.getTextSize(button_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
    text_x = button_top_left[0] + (button_bottom_right[0] - button_top_left[0] - text_size[0]) // 2
    text_y = button_top_left[1] + (button_bottom_right[1] - button_top_left[1] + text_size[1]) // 2
    cv2.putText(frame, button_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    landmarks_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmarks_points:
        landmarks = landmarks_points[0].landmark
        for index, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if index == 1:
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]
        right = [landmarks[475], landmarks[477]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        for landmark in right:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 0, 255))

        if reading_mode:
            dist_cent = (screen_y - (frame.shape[0] / 2)) / 20
            pyautogui.vscroll(dist_cent)

        if (right[0].y - right[1].y) > -0.024:
            print("Right Click")
            pyautogui.rightClick()
            pyautogui.sleep(0.5)
        elif (left[0].y - left[1].y) < 0.01:
            print("Click")
            pyautogui.click()
            pyautogui.sleep(0.5)

    cv2.imshow("Sign Bridge: WL", frame)
    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()
