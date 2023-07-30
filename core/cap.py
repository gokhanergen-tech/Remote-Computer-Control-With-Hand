from concurrent.futures import ThreadPoolExecutor
from math import sqrt
import cv2
import mediapipe as mp
import psutil
from entities.mouse import Mouse
from win32api import GetSystemMetrics

grabSize = 50

pool = ThreadPoolExecutor(max_workers=psutil.cpu_count())
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5
                       )

mp_draw = mp.solutions.drawing_utils
mouse = Mouse(GetSystemMetrics(0), GetSystemMetrics(1))


def resolution(cap, w, h):
    cap.set(3, w)
    cap.set(4, h)


def isExist(value):
    return bool(value)


def getDistance(a, b, hands_landmarks, scale=False, w=0, h=0):
    dx = hands_landmarks[0].landmark[a].x - hands_landmarks[0].landmark[b].x
    dy = hands_landmarks[0].landmark[a].y - hands_landmarks[0].landmark[b].y
    if (not scale):
        return sqrt(dx ** 2 + dy ** 2)
    else:
        return sqrt((dx * w) ** 2 + (dy * h) ** 2)


def draw(frame, hands_landmarks):
    h, w, c = frame.shape

    distance_three_to_seventeen = round(getDistance(3, 17, hands_landmarks, True, w, h))
    distance_zero_to_ten = round(getDistance(0, 10, hands_landmarks, True, w, h))
    distance_left = getDistance(4, 8, hands_landmarks)
    distance_double_click = getDistance(4, 12, hands_landmarks)
    distance_point = getDistance(9, 0, hands_landmarks)
    distance_right = getDistance(16, 4, hands_landmarks)
    distance_width = getDistance(4, 20, hands_landmarks)
    distance_height = getDistance(0, 12, hands_landmarks)

    wrapped_frame = frame[int(distance_zero_to_ten):int(h - distance_zero_to_ten),
                    int(distance_three_to_seventeen):int(w - distance_three_to_seventeen)]


    wh, ww, wc = wrapped_frame.shape
    wx = w * (hands_landmarks[0].landmark[0].x + hands_landmarks[0].landmark[9].x) / 2 - distance_three_to_seventeen
    wy = h * (hands_landmarks[0].landmark[0].y + hands_landmarks[0].landmark[9].y) / 2 - distance_zero_to_ten

    if (wx < 0):
        wx = 1
    if (wy < 0):
        wy = 1

    try:
        x = round((wx) * (mouse._swidth / (ww)))
        y = round((wy) * (mouse._sheight / (wh)))
    except ZeroDivisionError:
        return

    mouse.move(mouse._swidth - x + (0 if (mouse._swidth - x) < mouse._swidth / 2 else distance_width), y +
               (0 if (mouse._sheight - y) < mouse._sheight / 2 else distance_height))

    if (distance_left * 100 < distance_point * 100 / 5):
        mouse.click()
    elif (distance_right * 100 < distance_point * 100 / 5):
        mouse.click(button="right")
    elif (distance_double_click * 100 < distance_point * 100 / 5):
        mouse.click(button="double")


def start(cam_code=0):
    cap = cv2.VideoCapture(cam_code)

    while (True):
        ret, frame = cap.read()
        if not ret:
            print("failed to grab frame")
            break
        frame = cv2.GaussianBlur(frame, (3, 3), 0)
        grappedImage = frame[grabSize:frame.shape[0] - grabSize, grabSize:frame.shape[1] - grabSize]

        rgb_img = cv2.cvtColor(grappedImage, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_img)
        hands_landmarks = results.multi_hand_landmarks

        if (isExist(hands_landmarks)):

            try:
                cv2.imshow("hand", grappedImage[int(grappedImage.shape[0] * hands_landmarks[0].landmark[12].y):
                                                int(grappedImage.shape[0] * hands_landmarks[0].landmark[12].y + int(
                                                    grappedImage.shape[0] * hands_landmarks[0].landmark[0].y) - int(
                                                    grappedImage.shape[0] * hands_landmarks[0].landmark[12].y)),
                                   int(grappedImage.shape[1] * hands_landmarks[0].landmark[20].x):int(
                                       grappedImage.shape[1] * hands_landmarks[0].landmark[20].x) + int(
                                       grappedImage.shape[1] * hands_landmarks[0].landmark[4].x) - int(
                                       grappedImage.shape[1] * hands_landmarks[0].landmark[20].x)])
            except:
                pass;
            pool.submit(draw, grappedImage, hands_landmarks)

        cv2.imshow("Hand tracer", grappedImage)
        if (cv2.waitKey(1) == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()
