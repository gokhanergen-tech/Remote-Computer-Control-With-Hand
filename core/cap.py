import cv2
import mediapipe as mp
import time
from entities.mouse import Mouse
from math import sqrt
from win32api import GetSystemMetrics;

mp_hands=mp.solutions.hands

hands=mp_hands.Hands(static_image_mode=False,
 max_num_hands=1,
 min_detection_confidence=0.2,
 min_tracking_confidence=0.5
 )

mp_draw=mp.solutions.drawing_utils;
mouse=Mouse(GetSystemMetrics(0),GetSystemMetrics(1))
def resolution(cap,w,h):
       cap.set(3,w);
       cap.set(4,h)

def isExist(value):
     return bool(value)

def getDistance(a,b,hands_landmarks,scale=False,w=0,h=0):
     dx=hands_landmarks[0].landmark[a].x-hands_landmarks[0].landmark[b].x;
     dy=hands_landmarks[0].landmark[a].y-hands_landmarks[0].landmark[b].y;
     if(not scale):
      return sqrt(dx**2+dy**2);
     else:
      return sqrt((dx*w)**2+(dy*h)**2);

def draw(frame,hands_landmarks):
     h,w,c=frame.shape
   

     distance_three_to_seventeen=round(getDistance(3,17,hands_landmarks,True,w,h))
     distance_zero_to_ten=round(getDistance(0,10,hands_landmarks,True,w,h))
     distance_left=getDistance(4,8,hands_landmarks);
     distance_double_click=getDistance(4,12,hands_landmarks);
     distance_point=getDistance(9,0,hands_landmarks);
     distance_right=getDistance(16,4,hands_landmarks)

     wrapped_frame=frame[int(distance_zero_to_ten):int(h-distance_zero_to_ten),int(distance_three_to_seventeen):int(w-distance_three_to_seventeen)]

     x=1;
     y=1
     
     wh,ww,wc=wrapped_frame.shape;
     wx=(hands_landmarks[0].landmark[0].x*w+hands_landmarks[0].landmark[9].x*w)/2-distance_three_to_seventeen;
     wy=(hands_landmarks[0].landmark[0].y*h+hands_landmarks[0].landmark[9].y*h)/2-distance_zero_to_ten;
     if(wx<0):
         wx=1;
     if(wy<0):
         wy=1;
     try:
      x=round((wx)*(mouse._swidth/(ww)))
      y=round((wy)*(mouse._sheight/(wh)))
     except ZeroDivisionError:
         x=1;
         y=1;
         pass
     
     mouse.move(mouse._swidth-x,y)
     if(distance_left*100<distance_point*100/4):
           mouse.click()
     if(distance_right*100<distance_point*100/4):
           mouse.click(button="right")
     if(distance_double_click*100<distance_point*100/4):
           mouse.click(button="double")
          

     """for hand_lms in hands_landmarks:
         for id,landmark in enumerate(hand_lms.landmark):
             h,w,c=frame.shape
             cx=int(w*landmark.x);
             cy=int(h*landmark.y);
			 
             cv2.circle(frame,(cx,cy),2,(255,0,0))
         mp_draw.draw_landmarks(frame,hand_lms,mp_hands.HAND_CONNECTIONS)"""

def start(cam_code=0):
    
 cap=cv2.VideoCapture(cam_code);
 resolution(cap,640,480)
 while(True):
    ret,frame=cap.read();
   
    frame=cv2.GaussianBlur(frame,(3,3),0)
 
    rgb_img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB);
    results=hands.process(rgb_img)
    hands_landmarks=results.multi_hand_landmarks;
    if(isExist(hands_landmarks)):
       draw(frame,hands_landmarks)
    cv2.imshow("Hand tracer",frame)
    if(cv2.waitKey(1)==ord('q')):
        break
 cap.release();
 cv2.destroyAllWindows();