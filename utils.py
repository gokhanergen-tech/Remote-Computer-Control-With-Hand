def cam_control(code):
   cap=__import__("cv2").VideoCapture(code);
   res,frame=cap.read()
   __import__("cv2").imshow("test",frame)
   __import__("cv2").destroyAllWindows();
   cap.release();