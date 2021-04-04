import numpy as np
import cv2
from mainCamera import MainCamera
from leftSideCamera import LeftSideCamera
from rightSideCamera import RightSideCamera
#import time

class DrivingProcessing:
    def __init__(self, w, h, camera):
        self.w = w
        self.h = h
        self.camera = camera
        self.avgOfCams = int(h/2)

    def drivingFunction(self):
        cap_left = cv2.VideoCapture(0)
        cap_right = cv2.VideoCapture(1)
        cap_left.set(3, self.w)
        cap_left.set(4, self.h)
        cap_right.set(3, self.w)
        cap_right.set(4, self.h)
        left_side_camera = LeftSideCamera()
        right_side_camera = RightSideCamera()
        while(True):
            _left, frame_left = cap_left.read()
            _right, frame_right = cap_right.read()
            if self.camera == "MainCamera":
                mainCamera = MainCamera(np.array(frame_left))
                self.forward, self.left, self.right = mainCamera.capturingFunction()
            elif self.camera == "SideCamera":
                self.forward, self.left, self.right, self.errorLeft, self.Left_avgY = left_side_camera.capturingFunction(np.array(frame_left))
                #bu verilerle asagıdakiler çakışıyor(rightSideCamera'nın fonksiyonundan atanan degerler, 4 satır aşağısı) o yüzden bunları değişkende tutacagız
                t_forward, t_left, t_right = self.forward, self.left, self.right
                self.forward, self.left, self.right, self.errorRight, self.Right_avgY = right_side_camera.capturingFunction(np.array(frame_right))
                if self.errorLeft is True and self.errorRight is True:
                    self.activity = "None"
                elif self.errorLeft is True and self.errorRight is False:
                    self.activity = "Right"
                elif self.errorLeft is False and self.errorRight is True:
                    self.forward, self.left, self.right = t_forward, t_left, t_right
                    self.activity = "Left"
                elif self.errorLeft is False and self.errorRight is False:
                    if abs(avgOfCams - self.Left_avgY) <=  abs(avgOfCams - self.Right_avgY):
                        self.forward, self.left, self.right = t_forward, t_left, t_right
                        self.activity = "Left"
                    else:
                        self.activity = "Right" 
            else:
                print("Wrong Camera Name!")
                break
            if self.activity is "None":
                print("No lane detected..")
            elif self.activity is "Right":
                print("Right lane is active")
                if self.right is True:
                    print("Turn Right")
                elif self.left is True:
                    print("Turn Left")
                else:
                    print("Go forward")
            elif self.activity is "Left":
                print("Left lane is active")
                if self.right is True:
                    print("Turn Right")
                elif self.left is True:
                    print("Turn Left")
                else:
                    print("Go forward")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap_left.release()
        cap_right.release()
        cv2.destroyAllWindows()