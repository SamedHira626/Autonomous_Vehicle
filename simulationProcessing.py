import numpy as np
import cv2
import time
from mainCamera import MainCamera
from leftSideCamera import LeftSideCamera
from rightSideCamera import RightSideCamera
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MouseController
from PIL import ImageGrab
import pyautogui
import win32api

class SimulationProcessing:
    def __init__(self,camera):
        self.camera = camera
        self.left = False
        self.right = False
        self.forward = True
        self.errorLeft = False
        self.errorRight = False
        self.activity = "None"
        self.frameCount = 0
        self.Left_avgY = -1
        self.Right_avgY = -1
        #-------------------------
        self.leftLaneCheck = [1,1,1]
        self.rightLaneCheck = [1,1,1]
        self.leftAllOne = 1
        self.leftAllZero = 0
        self.rightAllOne = 1
        self.rightAllZero = 0
        self.missionRightTurn = False
        self.missionRightTurn_done = False
        self.missionLeftTurn = False
        self.missionLeftTurn_done = False
        #-------------------------
        """
        0-Sola dönülmez
        1-Sağa dönülmez
        2-Taşıt trafiğine kapalı yol
        3-Durak
        4-Trafik lambası (-1 ise yok demektir) 0-kırmızı 1-sarı 2-yeşil
        5-Dur
        """
        self.sign_lists = [0,0,0,0,-1,0]
        self.found_best = False
        self.LLC = False
        self.RLC = False
        self.brake = False
        self.brakeForStop = False
        self.brakeForStop_inArea = False
        self.brakeForDur = False
        self.brakeForDur_inArea = False

    def click_coordinates(self):
        """
        If the key state changes, get the positions
        """
        for pos in range(2):
            state_prev = win32api.GetKeyState(0x01)
            while True:
                state_current = win32api.GetKeyState(0x01)
                if state_current != state_prev:
                    pos = pyautogui.position()
                    print("**Positions set: ", pos)
                    return pos

    def set_pos(self):
        print('\n*Select first corner of the left cam')
        mouse_posX1, mouse_posY1 = self.click_coordinates()
        time.sleep(0.8)
        print('\n*Select second corner of the left cam')
        mouse_posX2, mouse_posY2 = self.click_coordinates()
        time.sleep(0.8)
        self.x = int(mouse_posX1)
        self.y = int(mouse_posY1)
        self.w = int(mouse_posX2)
        self.h = int(mouse_posY2)
        print("First area has been set!")
        print('\n*Select first corner of the right cam')
        mouse_posX1, mouse_posY1 = self.click_coordinates()
        time.sleep(0.8)
        print('\n*Select second corner of the right cam')
        mouse_posX2, mouse_posY2 = self.click_coordinates()
        time.sleep(0.8)
        self.xR = int(mouse_posX1)
        self.yR = int(mouse_posY1)
        self.wR = int(mouse_posX2)
        self.hR = int(mouse_posY2)
        print("Second area has been set!")
        print('\n*Select first corner of the area of traffic signs')
        mouse_posX1, mouse_posY1 = self.click_coordinates()
        time.sleep(0.8)
        print('\n*Select second corner of the area of traffic signs')
        mouse_posX2, mouse_posY2 = self.click_coordinates()
        time.sleep(0.8)
        self.xSigns = int(mouse_posX1)
        self.ySigns = int(mouse_posY1)
        self.wSigns = int(mouse_posX2)
        self.hSigns = int(mouse_posY2)
        print("Third area has been set!")
            
    def colorTesting(self,sign_img,mean_height_of_sign):
        points = np.array([[0,0,0]])
        #değişimler 255 0 0 ve 86 188 106
        #print(sign_img[12][47])
        i = 0
        px_difference = 71
        starting_px = 50
        px = starting_px
        while i<11:
            #gostermek amaclı siyaha atama
            #sign_img[mean_height_of_sign][px] = [0,0,0]
            if i == 0:
                points[0] = sign_img[mean_height_of_sign][px]
            else:
                points = np.append(points,[sign_img[mean_height_of_sign][px]],axis=0)
            px += px_difference
            i += 1
        self.points = points
        #print(self.points[9])
        cv2.imshow("Signs",sign_img)
    
    def lane_change_control(self):
        #sol şeritte hata yoksa atılacak değer 1 olur
        if self.errorLeft is False:
            self.leftLaneCheck[self.frameCount%3] = 1
            if self.leftLaneCheck[0] == 1 and self.leftLaneCheck[1] == 1 and self.leftLaneCheck[2] == 1:
                self.leftAllOne = 1
                if self.leftAllZero != 0:
                    #eger [1,1,1] olduysa ve [0,0,0]dan döndüyse şerit değişimi olmuştur
                    self.missionRightTurn = True
                    self.missionRightTurn_done = True
                    self.leftAllZero = 0
                else:
                    self.missionRightTurn = False
        #sol şeritte hata varsa atılacak değer 0 olur        
        else:
            self.leftLaneCheck[self.frameCount%3] = 0
            if self.leftLaneCheck[0] == 0 and self.leftLaneCheck[1] == 0 and self.leftLaneCheck[2] == 0:
                self.leftAllZero = 1
                if self.leftAllOne != 0:
                    #eger [0,0,0] olduysa ve [1,1,1]den döndüyse şerit değişimi olmuştur
                    self.missionRightTurn = True
                    self.missionRightTurn_done = True
                    self.leftAllOne = 0
                else:
                    self.missionRightTurn = False
        #sağ şeritte hata yoksa atılacak değer 1 olur
        if self.errorRight is False:
            self.rightLaneCheck[self.frameCount%3] = 1
            if self.rightLaneCheck[0] == 1 and self.rightLaneCheck[1] == 1 and self.rightLaneCheck[2] == 1:
                self.rightAllOne = 1
                if self.rightAllZero != 0:
                    #eger [1,1,1] olduysa ve [0,0,0]dan döndüyse şerit değişimi olmuştur
                    self.missionLeftTurn = True
                    self.missionLeftTurn_done = True
                    self.rightAllZero = 0
                else:
                    self.missionLeftTurn = False
        #sağ şeritte hata yoksa atılacak değer 0 olur
        else:
            self.rightLaneCheck[self.frameCount%3] = 0
            if self.rightLaneCheck[0] == 0 and self.rightLaneCheck[1] == 0 and self.rightLaneCheck[2] == 0:
                self.rightAllZero = 1
                if self.rightAllOne != 0:
                    #eger [0,0,0] olduysa ve [1,1,1]den döndüyse şerit değişimi olmuştur
                    self.missionLeftTurn = True
                    self.missionLeftTurn_done = True
                    self.rightAllOne = 0
                else:
                    self.missionLeftTurn = False
        if self.missionRightTurn == True:
            #[0,0,0] dan [1,1,1] e ya da tam tersi oldugu zaman şerit değişimini alıyoruz
            print("Left Lane change!!")
            self.LLC = True
        if self.missionLeftTurn == True:
            #[0,0,0] dan [1,1,1] e ya da tam tersi oldugu zaman şerit değişimini alıyoruz
            print("Right Lane change!!")
            self.RLC = True

    def traffic_sign_feedback_with_unity_features(self):
        if ((self.points[0] == [86,188,106]).all() or (self.points[4] == [86,188,106]).all()) or (self.points[3] == [86,188,106]).all():
            self.sign_lists[0] = 1
        if ((self.points[1] == [86,188,106]).all() or (self.points[5] == [86,188,106]).all()) or (self.points[2] == [86,188,106]).all():
            self.sign_lists[1] = 1
        if (self.points[6] == [86,188,106]).all():
            self.sign_lists[2] = 1
        if (self.points[7] == [86,188,106]).all() or (self.points[8] == [86,188,106]).all():
            self.sign_lists[3] = 1
            self.brakeForStop_inArea = True
        if (self.points[7] == [255,0,0]).all() and (self.points[8] == [255,0,0]).all():
            self.sign_lists[3] = 0
        
        if (self.points[9] == [255,0,0]).all():
            self.sign_lists[4] = 0
        elif (self.points[9] == [232,158,51]).all():
            self.sign_lists[4] = 1
        elif (self.points[9] == [88,183,107]).all():
            self.sign_lists[4] = 2
        else:
            self.sign_lists[4] = -1
        if (self.points[10] == [86,188,106]).all():
            self.sign_lists[5] = 1
            self.brakeForDur_inArea = True
        if (self.points[10] == [255,0,0]).all():
            self.sign_lists[5] = 0

    """def traffic_sign_feedback_with_unity_features(self):
        #sola dönüş yasak ve ileri sağa mecburi yön YAPILDI
        if self.traffic_signs_list[3] == 1 or self.traffic_signs_list[5] == 1 or self.traffic_signs_list[8] == 1:
            self.sign_lists[0] = 1
        #saga dönüş yasak ve ileri sola mecburi yön YAPILDI
        if self.traffic_signs_list[4] == 1 or self.traffic_signs_list[6] == 1 or self.traffic_signs_list[7] == 1:
            self.sign_lists[1] = 1
        #tasıt trafiğine kapalı yol, YAPILMADI!!!
        if self.traffic_signs_list[15] == 1 or self.traffic_signs_list[16]:
            self.sign_lists[2] = 1
        #durak YAPILDI
        if self.traffic_signs_list[2] == 1:
            self.sign_lists[3] = 1
            self.brakeForStop_inArea = True
        elif self.traffic_signs_list[2] == 0:
            self.sign_lists[3] = 0
        #trafik lambası 12 yeşil 13 kırmızı 14 sarı demek YAPILDI
        if self.traffic_signs_list[12] == 1:
            self.sign_lists[4] = 2
        elif self.traffic_signs_list[13] == 1:
            self.sign_lists[4] = 0
        elif self.traffic_signs_list[14] == 1:
            self.sign_lists[4] = 1
        if self.traffic_signs_list[12] == 0 and self.traffic_signs_list[13] == 0 and self.traffic_signs_list[14] == 0:
            self.sign_lists[4] = -1
        #dur YAPILDI
        if self.traffic_signs_list[9] == 1:
            self.sign_lists[5] = 1
            self.brakeForDur_inArea = True
        elif self.traffic_signs_list[9] == 0:
            self.sign_lists[5] = 0"""
    
    def running_type(self):
        print("Which type do you want to run the code with(Deep learning:1, Unity features: 2)")
        choice = int(input())
        if choice == 1:
            self.running_type = "Deep_learning"
        elif choice == 2:
            self.running_type = "Unity_features"
        else:
            print("Wrong input!")
            exit

    def running_with_unity_features(self,keyboard,left_side_camera,right_side_camera):
        frame_left = ImageGrab.grab((self.x, self.y, self.w, self.h)) 
        self.forward, self.left, self.right,self.errorLeft, self.Left_avgY = left_side_camera.capturingFunction(np.array(frame_left))
        #bu verilerle asagıdakiler çakışıyor(rightSideCamera'nın fonksiyonundan atanan degerler, 4 satır aşağısı) o yüzden bunları değişkende tutacagız
        t_forward, t_left, t_right = self.forward, self.left, self.right
        frame_right = ImageGrab.grab((self.xR, self.yR, self.wR, self.hR))
        self.forward, self.left, self.right, self.errorRight, self.Right_avgY = right_side_camera.capturingFunction(np.array(frame_right))
        
        signs_img = ImageGrab.grab((self.xSigns,self.ySigns,self.wSigns,self.hSigns))
        self.mean_height_of_signs = int((self.hSigns - self.ySigns)/2)
        self.colorTesting(np.array(signs_img),self.mean_height_of_signs)
        
        #şerit değişim kontrol mekanizması
        self.lane_change_control()

        #trafik levha dönütleri - unity özellikleriyle
        self.traffic_sign_feedback_with_unity_features()

        #KAMERALARDAN GELEN VERİLERİN İŞLENMESİ BAŞLANGICI
        if self.sign_lists[4] == -1 or self.sign_lists[4] == 2:
            if self.brake is True:
                keyboard.release(Key.space)
                keyboard.press('s')
                time.sleep(0.2)
                keyboard.release('s')
                self.brake = False
            if self.sign_lists[4] == 2:
                if self.frameCount %4 == 0:
                    print("GREEN LIGHT!")
            if self.brakeForStop_inArea == True and self.sign_lists[3] == 0:
                print("STOP!")
                self.brakeForStop = True
                self.activity = "Stop"
            if self.brakeForDur_inArea == True and self.sign_lists[5] == 0:
                print("Dur!")
                self.brakeForDur = True
                self.activity = "Dur"
            if self.brakeForStop == False and self.brakeForDur is False:
                if self.sign_lists[0] == 0 and self.sign_lists[1] == 0:
                    if self.errorLeft is True and self.errorRight is True:
                        self.activity = "None"
                    elif self.errorLeft is True and self.errorRight is False:
                        self.activity = "Right"
                    elif self.errorLeft is False and self.errorRight is True:
                        self.forward, self.left, self.right = t_forward, t_left, t_right
                        self.activity = "Left"
                    elif self.errorLeft is False and self.errorRight is False:
                        if abs(self.middle_line - self.Left_avgY) <=  abs(self.middle_line - self.Right_avgY):
                            self.forward, self.left, self.right = t_forward, t_left, t_right
                            self.activity = "Left"
                        else:
                            self.activity = "Right"
                else:
                    if self.sign_lists[0] == 1 and self.sign_lists[1] == 0:
                        if self.frameCount %4 == 0:
                            print("LEFT TURN FORBIDDEN")
                        if self.errorRight is False:
                            self.activity = "Right"
                            #şerit değişimi tamamlandıysa ve sol şerit ile sağ şerit arasındaki y pixel farkı 20den küçükse tekrardan şerit aramaya devam edecek
                            if (abs(abs(self.middle_line - self.Left_avgY) - abs(self.middle_line - self.Right_avgY)) <= int(self.middle_line*2/10) ) and self.missionRightTurn_done is True:
                                print("Turning Right Done!")
                                self.missionRightTurn_done = False
                                self.sign_lists[0] = 0
                        else:
                            self.activity = "None"
                    elif self.sign_lists[1] == 1 and self.sign_lists[0] == 0:
                        if self.frameCount %4 == 0:
                            print("RIGHT TURN FORBIDDEN")
                        if self.errorLeft is False:
                            self.forward, self.left, self.right = t_forward, t_left, t_right
                            self.activity = "Left"
                            #şerit değişimi tamamlandıysa ve sol şerit ile sağ şerit arasındaki y pixel farkı 20den küçükse tekrardan şerit aramaya devam edecek
                            if (abs(abs(self.middle_line - self.Left_avgY) - abs(self.middle_line - self.Right_avgY)) <= int(self.middle_line*2/10) ) and self.missionLeftTurn_done is True:
                                print("Turning Left Done!")
                                self.missionLeftTurn_done = False
                                self.sign_lists[1] = 0
                        else:
                            self.activity = "None"
                    elif self.sign_lists[1] == 1 and self.sign_lists[0] == 1:
                        #SIKINTILI İŞ SENSÖRLE OLMALI
                        if self.frameCount %4 == 0:
                            print("LEFT AND RIGHT TURN FORBIDDEN")
                        if (abs(abs(self.middle_line - self.Left_avgY) - abs(self.middle_line - self.Right_avgY)) <= int(self.middle_line*2/10) ) and self.found_best is False:
                            self.found_best = True
                        if self.found_best is True:
                            self.left = False
                            self.right = False
                            self.forward = True
                            self.activity = "forward"
                            if (self.RLC is True) and (self.LLC is True):
                                if self.errorLeft is False or self.errorRight is False:
                                    if abs(self.middle_line - self.Left_avgY) <= int(self.middle_line*2/10) or abs(self.middle_line - self.Right_avgY) <= int(self.middle_line*2/10):
                                        print("Way Found Back!")
                                        self.sign_lists[1] = 0 
                                        self.sign_lists[0] = 0
                                        self.found_best = False
                                        self.LLC = False
                                        self.RLC = False
                                
        elif self.sign_lists[4] == 0 or self.sign_lists[4] == 1:
            if self.sign_lists[4] == 1:
                if self.frameCount %4 == 0:
                    print("RED LIGHT!")
            else:
                if self.frameCount %4 == 0:
                    print("YELLOW LIGHT!")
            #freezing işlemi gelecek buraya
            self.activity = "Brake"
            self.brake = True

    def running_with_deep_learning(self,keyboard):
        img = ImageGrab.grab((self.x, self.y, self.w, self.h))
        sideCamera = LeftSideCamera(np.array(img))
        self.forward, self.left, self.right,self.errorLeft, self.Left_avgY = sideCamera.capturingFunction()
        #bu verilerle asagıdakiler çakışıyor(rightSideCamera'nın fonksiyonundan atanan degerler, 4 satır aşağısı) o yüzden bunları değişkende tutacagız
        t_forward, t_left, t_right = self.forward, self.left, self.right
        img1 = ImageGrab.grab((self.xR, self.yR, self.wR, self.hR))
        rightSideCamera = RightSideCamera(np.array(img1))
        self.forward, self.left, self.right, self.errorRight, self.Right_avgY = rightSideCamera.capturingFunction()
        
        """

        BURADA DEEP LEARNİNGE GİDECEK RESİM OLACAK

        signs_img = ImageGrab.grab((self.xSigns,self.ySigns,self.wSigns,self.hSigns))
        self.traffic_signs_list = deep_learning(np.array(signs_img))
        
        """
        #şerit değişim kontrol mekanizması
        self.lane_change_control()

        #trafik levha dönütleri - deep learningle
        self.traffic_sign_feedback_with_deep_learning()

        #KAMERALARDAN GELEN VERİLERİN İŞLENMESİ BAŞLANGICI
        if self.sign_lists[4] == -1 or self.sign_lists[4] == 2:
            if self.brake is True:
                keyboard.release(Key.space)
                keyboard.press('s')
                time.sleep(0.2)
                keyboard.release('s')
                self.brake = False
            if self.sign_lists[4] == 2:
                if self.frameCount %4 == 0:
                    print("GREEN LIGHT!")
            if self.brakeForStop_inArea == True and self.sign_lists[3] == 0:
                print("STOP!")
                self.brakeForStop = True
                self.activity = "Stop"
            if self.brakeForDur_inArea == True and self.sign_lists[5] == 0:
                print("Dur!")
                self.brakeForDur = True
                self.activity = "Dur"
            if self.brakeForStop == False and self.brakeForDur is False:
                if self.sign_lists[0] == 0 and self.sign_lists[1] == 0:
                    if self.errorLeft is True and self.errorRight is True:
                        self.activity = "None"
                    elif self.errorLeft is True and self.errorRight is False:
                        self.activity = "Right"
                    elif self.errorLeft is False and self.errorRight is True:
                        self.forward, self.left, self.right = t_forward, t_left, t_right
                        self.activity = "Left"
                    elif self.errorLeft is False and self.errorRight is False:
                        if abs(self.avgOfCams - self.Left_avgY) <=  abs(self.avgOfCams - self.Right_avgY):
                            self.forward, self.left, self.right = t_forward, t_left, t_right
                            self.activity = "Left"
                        else:
                            self.activity = "Right"
                else:
                    if self.sign_lists[0] == 1 and self.sign_lists[1] == 0:
                        if self.frameCount %4 == 0:
                            print("LEFT TURN FORBIDDEN")
                        if self.errorRight is False:
                            self.activity = "Right"
                            #şerit değişimi tamamlandıysa ve sol şerit ile sağ şerit arasındaki y pixel farkı 20den küçükse tekrardan şerit aramaya devam edecek
                            if (abs(abs(self.avgOfCams - self.Left_avgY) - abs(self.avgOfCams - self.Right_avgY)) <= 20 ) and self.missionRightTurn_done is True:
                                print("Turning Right Done!")
                                self.missionRightTurn_done = False
                                self.sign_lists[0] = 0
                        else:
                            self.activity = "None"
                    elif self.sign_lists[1] == 1 and self.sign_lists[0] == 0:
                        if self.frameCount %4 == 0:
                            print("RIGHT TURN FORBIDDEN")
                        if self.errorLeft is False:
                            self.forward, self.left, self.right = t_forward, t_left, t_right
                            self.activity = "Left"
                            #şerit değişimi tamamlandıysa ve sol şerit ile sağ şerit arasındaki y pixel farkı 20den küçükse tekrardan şerit aramaya devam edecek
                            if (abs(abs(self.avgOfCams - self.Left_avgY) - abs(self.avgOfCams - self.Right_avgY)) <= 20 ) and self.missionLeftTurn_done is True:
                                print("Turning Left Done!")
                                self.missionLeftTurn_done = False
                                self.sign_lists[1] = 0
                        else:
                            self.activity = "None"
                    elif self.sign_lists[1] == 1 and self.sign_lists[0] == 1:
                        #SIKINTILI İŞ SENSÖRLE OLMALI
                        if self.frameCount %4 == 0:
                            print("LEFT AND RIGHT TURN FORBIDDEN")
                        if (abs(abs(self.avgOfCams - self.Left_avgY) - abs(self.avgOfCams - self.Right_avgY)) <= 15 ) and self.found_best is False:
                            self.found_best = True
                        if self.found_best is True:
                            self.left = False
                            self.right = False
                            self.forward = True
                            self.activity = "forward"
                            if (self.RLC is True) and (self.LLC is True):
                                if self.errorLeft is False or self.errorRight is False:
                                    if abs(self.avgOfCams - self.Left_avgY) <= 20 or abs(self.avgOfCams - self.Right_avgY) <=20:
                                        print("Way Found Back!")
                                        self.sign_lists[1] = 0 
                                        self.sign_lists[0] = 0
                                        self.found_best = False
                                        self.LLC = False
                                        self.RLC = False
                                
        elif self.sign_lists[4] == 0 or self.sign_lists[4] == 1:
            if self.sign_lists[4] == 1:
                if self.frameCount %4 == 0:
                    print("RED LIGHT!")
            else:
                if self.frameCount %4 == 0:
                    print("YELLOW LIGHT!")
            #freezing işlemi gelecek buraya
            self.activity = "Brake"
            self.brake = True
            
    def simulationFunction(self):
        self.running_type()
        self.set_pos()
        self.middle_line = int((self.h - self.y)/2)
        keyboard = Controller()
        left_side_camera = LeftSideCamera()
        right_side_camera = RightSideCamera()
        time.sleep(3)
        while(True):
            self.frameCount += 1
            if self.running_type == "Unity_features":
                self.running_with_unity_features(keyboard,left_side_camera,right_side_camera)
            elif self.running_type == "Deep_learning":
                self.running_with_deep_learning(keyboard)
            
            #GELEN VERİLERE GÖRE ARACI HAREKET ETTİRDİĞİMİZ YER BAŞLANGICI
            if self.activity is "None":
                self.noAction(keyboard)
            elif self.activity is "Brake":
                self.braking(keyboard)
            elif self.activity is "Stop":
                self.stopping(keyboard)
            elif self.activity is "Dur":
                self.dur(keyboard)
            else:
                self.throttleActive(keyboard)
                if self.left == True:
                    self.turnLeft(keyboard)
                if self.right == True:
                    self.turnRight(keyboard)
                if self.forward == True:
                    self.goForward(keyboard)
            #self.throttlePassive(keyboard)
            
            #keyboard.release('p')
            #GELEN VERİLERE GÖRE ARACI HAREKET ETTİRDİĞİMİZ YER SONU

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        keyboard.release('w')
    
    def throttleActive(self, keyboard):
        keyboard.press('w')
    
    def throttlePassive(self, keyboard):
        keyboard.release('w')

    def turnLeft(self, keyboard):
        keyboard.release('d')
        keyboard.press('a')

    def turnRight(self, keyboard):
        keyboard.release('a')
        keyboard.press('d')
    
    def goForward(self, keyboard):
        keyboard.release('a')
        keyboard.release('d')

    def noAction(self, keyboard):
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('d')
    
    def braking(self, keyboard):
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release('s')
        keyboard.press(Key.space)

    def stopping(self, keyboard):
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release('s')
        keyboard.press(Key.space)
        time.sleep(8)
        keyboard.release(Key.space)
        keyboard.press('s')
        time.sleep(0.2)
        keyboard.release('s')
        self.brakeForStop = False
        self.brakeForStop_inArea = False

    def dur(self, keyboard):
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release('s')
        keyboard.press(Key.space)
        time.sleep(8)
        keyboard.release(Key.space)
        keyboard.press('s')
        time.sleep(0.2)
        keyboard.release('s')
        self.brakeForDur = False
        self.brakeForDur_inArea = False
