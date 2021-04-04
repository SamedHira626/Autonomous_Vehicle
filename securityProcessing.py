from pynput.mouse import Controller as MouseController
import time
import numpy as np
import cv2
from PIL import ImageGrab
from imageProcessing import ImageProcessing

class SecurityProcessing:
    def __init__(self):
        self.areas = None

    def processFunc(self, image):
        self.areas = [0, 0, 0, 0, 0]#F, FR, FL, R, L
        maskedGreenImage, maskedRedImage = self.gettingImage(image)
        forwardPointsInfo = [int(np.size(maskedGreenImage, 0) * 0.1515), int(0.5 * np.size(maskedGreenImage, 1)), 0]#y, x, kind  (0 means forward)
        forwardRightPointsInfo = [int(np.size(maskedGreenImage, 0) * 0.2554), int(0.66 * np.size(maskedGreenImage, 1)), 1]#y, x, kind  (1 means forward and right)
        forwardLeftPointsInfo = [int(np.size(maskedGreenImage, 0) * 0.2554), int(0.34 * np.size(maskedGreenImage, 1)), 2]#y, x, kind  (2 means forward and left)
        RightPointsInfo = [int(np.size(maskedGreenImage, 0) * 0.4978), int(0.75 * np.size(maskedGreenImage, 1)), 3]#y, x, kind  (3 means right)
        LeftPointsInfo = [int(np.size(maskedGreenImage, 0) * 0.4978), int(0.25 * np.size(maskedGreenImage, 1)), 4]#y, x, kind  (4 means left)
        #print("forwardPointsInfo", maskedGreenImage[forwardPointsInfo[0]][forwardPointsInfo[1]])
        self.controllingSensors(maskedGreenImage, maskedRedImage, forwardPointsInfo)
        self.controllingSensors(maskedGreenImage, maskedRedImage, forwardRightPointsInfo)
        self.controllingSensors(maskedGreenImage, maskedRedImage, forwardLeftPointsInfo)
        self.controllingSensors(maskedGreenImage, maskedRedImage, LeftPointsInfo)
        self.controllingSensors(maskedGreenImage, maskedRedImage, RightPointsInfo)
        return self.areas

    def gettingImage(self, img):
        greenLowerColor = np.array([40, 40, 40])
        greenUpperColor = np.array([70, 255, 255])
        redLowerColor = np.array([110,50,50])
        redUpperColor = np.array([130,255,255])
        maskedGreenImage = ImageProcessing.colorDetection(self, img, greenLowerColor, greenUpperColor)
        maskedRedImage = ImageProcessing.colorDetection(self, img, redLowerColor, redUpperColor)
        ImageProcessing.showingScreen(self, "Sensor", np.array(img))
        ImageProcessing.showingScreen(self, "Green", maskedGreenImage)
        ImageProcessing.showingScreen(self, "Red", maskedRedImage)
        return maskedGreenImage, maskedRedImage
    
    def controllingSensors(self, greenMaskedImageArray, redMaskedImageArray, coordinationArray):
        if coordinationArray[2] == 0:
            if greenMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("İLERİ YEŞİL BULUNDU")
                self.areas[0] = int(1)
            elif redMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("İLERİ KIRMIZI BULUNDU")
                self.areas[0] = int(2)
        if coordinationArray[2] == 1:
            if greenMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("İLERİ VE SAĞA YEŞİL BULUNDU")
                self.areas[1] = int(1)
            elif redMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("İLERİ VE SAĞA KIRMIZI BULUNDU")
                self.areas[1] = int(2)
        if coordinationArray[2] == 2:
            if greenMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("İLERİ VE SOLA YEŞİL BULUNDU")
                self.areas[2] = int(1)
            elif redMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("İLERİ VE SOLA KIRMIZI BULUNDU")
                self.areas[2] = int(2)
        if coordinationArray[2] == 3:
            if greenMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("SAĞA YEŞİL BULUNDU")
                self.areas[3] = int(1)
            elif redMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("SAĞA KIRMIZI BULUNDU")
                self.areas[3] = int(2)
        if coordinationArray[2] == 4:
            if greenMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("SOLA YEŞİL BULUNDU")
                self.areas[4] = int(1)
            elif redMaskedImageArray[coordinationArray[0]][coordinationArray[1]] == 255:
                print("SOLA KIRMIZI BULUNDU")
                self.areas[4] = int(2)