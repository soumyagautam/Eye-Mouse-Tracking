import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)

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

        if (right[0].y - right[1].y) > -0.024:
            print("Right Click")
            pyautogui.rightClick()
            pyautogui.sleep(0.5)
        elif (left[0].y - left[1].y) < 0.01:
            print("Click")
            pyautogui.click()
            pyautogui.sleep(0.5)

    cv2.imshow("Sign Bridge: WL", frame)
    cv2.waitKey(1)
