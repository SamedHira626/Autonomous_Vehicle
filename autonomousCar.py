from imageProcessing import ImageProcessing
from videoProcessing import VideoProcessing
from simulationProcessing import SimulationProcessing
from drivingProcessing import DrivingProcessing
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QLineEdit, QMainWindow
import sys
"""
class GUI(QMainWindow):
    def __init__(self, x, y, width, height, title):
        super(GUI, self).__init__()
        self.imageName = None
        self.videoName = None
        self.mainCamera = False
        self.sideCamera = False
        self.isImageVideoProcessingEnable = False
        self.isSimulationProcessingEnable = False
        self.isDrivingProcessingEnable = False
        self.setGeometry(x, y, width, height)
        self.setWindowTitle(title)
        self.initUI()

    def initUI(self):
        self.labelProcessChoiceText = QtWidgets.QLabel(self)
        self.labelProcessChoiceText.setText("Which process will you execute?")
        self.labelProcessChoiceText.move(375, 5)
        self.labelProcessChoiceText.resize(160, 20)

        self.buttonImageVideoProcessing = QtWidgets.QPushButton(self)
        self.buttonImageVideoProcessing.setText("Image & Video Processing")
        self.buttonImageVideoProcessing.move(0, 30)
        self.buttonImageVideoProcessing.resize(300, 40)
        self.buttonImageVideoProcessing.clicked.connect(self.imageVideoProcessingButtonClicked)

        self.labelImageName = QtWidgets.QLabel(self)
        self.labelImageName.setText("Image Path :")
        self.labelImageName.move(10, 80)
        self.labelImageName.setEnabled(False)

        self.buttonImageName = QtWidgets.QPushButton(self)
        self.buttonImageName.setText("Browse Image")
        self.buttonImageName.move(75, 85)
        self.buttonImageName.resize(100, 20)
        self.buttonImageName.clicked.connect(self.gettingImageName)
        self.buttonImageName.setEnabled(False)

        self.labelVideoName = QtWidgets.QLabel(self)
        self.labelVideoName.setText("Video Path :")
        self.labelVideoName.move(10, 100)
        self.labelVideoName.setEnabled(False)

        self.buttonVideoName = QtWidgets.QPushButton(self)
        self.buttonVideoName.setText("Browse Video")
        self.buttonVideoName.move(75, 105)
        self.buttonVideoName.resize(100, 20)
        self.buttonVideoName.clicked.connect(self.gettingVideoName)
        self.buttonVideoName.setEnabled(False)

        self.buttonSimulationProcessing = QtWidgets.QPushButton(self)
        self.buttonSimulationProcessing.setText("Simulation Processing")
        self.buttonSimulationProcessing.move(300, 30)
        self.buttonSimulationProcessing.resize(300, 40)
        self.buttonSimulationProcessing.clicked.connect(self.simulationProcessingButtonClicked)

        self.labelSimulationCameraText = QtWidgets.QLabel(self)
        self.labelSimulationCameraText.setText("Which camera will you use in the simulation?")
        self.labelSimulationCameraText.move(340, 80)
        self.labelSimulationCameraText.resize(220, 20)
        self.labelSimulationCameraText.setEnabled(False)

        self.labelSimulationCameraChoiceText = QtWidgets.QLabel(self)
        self.labelSimulationCameraChoiceText.setText("Camera Status : ")
        self.labelSimulationCameraChoiceText.move(370, 130)
        self.labelSimulationCameraChoiceText.resize(80, 20)
        self.labelSimulationCameraChoiceText.setEnabled(False)

        self.labelSimulationCameraChoiceValue = QtWidgets.QLabel(self)
        self.labelSimulationCameraChoiceValue.setText("None")
        self.labelSimulationCameraChoiceValue.move(460, 130)
        self.labelSimulationCameraChoiceValue.resize(80, 20)
        self.labelSimulationCameraChoiceValue.setEnabled(False)

        self.buttonSimulationMainCamera = QtWidgets.QPushButton(self)
        self.buttonSimulationMainCamera.setText("Main Camera")
        self.buttonSimulationMainCamera.move(320, 100)
        self.buttonSimulationMainCamera.resize(130, 30)
        self.buttonSimulationMainCamera.setEnabled(False)
        self.buttonSimulationMainCamera.clicked.connect(self.settingMainCamera)

        self.buttonSimulationSideCamera = QtWidgets.QPushButton(self)
        self.buttonSimulationSideCamera.setText("Side Camera")
        self.buttonSimulationSideCamera.move(450, 100)
        self.buttonSimulationSideCamera.resize(130, 30)
        self.buttonSimulationSideCamera.setEnabled(False)
        self.buttonSimulationSideCamera.clicked.connect(self.settingSideCamera)

        self.buttonDrivingProcessing = QtWidgets.QPushButton(self)
        self.buttonDrivingProcessing.setText("Driving Processing")
        self.buttonDrivingProcessing.move(600, 30)
        self.buttonDrivingProcessing.resize(300, 40)
        self.buttonDrivingProcessing.clicked.connect(self.drivingProcessingButtonClicked)

        self.labelDrivingCameraText = QtWidgets.QLabel(self)
        self.labelDrivingCameraText.setText("Which camera will you use in the driving?")
        self.labelDrivingCameraText.move(645, 80)
        self.labelDrivingCameraText.resize(220, 20)
        self.labelDrivingCameraText.setEnabled(False)

        self.buttonDrivingMainCamera = QtWidgets.QPushButton(self)
        self.buttonDrivingMainCamera.setText("Main Camera")
        self.buttonDrivingMainCamera.move(620, 100)
        self.buttonDrivingMainCamera.resize(130, 30)
        self.buttonDrivingMainCamera.setEnabled(False)
        self.buttonDrivingMainCamera.clicked.connect(self.settingMainCamera)

        self.buttonDrivingSideCamera = QtWidgets.QPushButton(self)
        self.buttonDrivingSideCamera.setText("Side Camera")
        self.buttonDrivingSideCamera.move(750, 100)
        self.buttonDrivingSideCamera.resize(130, 30)
        self.buttonDrivingSideCamera.setEnabled(False)
        self.buttonDrivingSideCamera.clicked.connect(self.settingSideCamera)

        self.labelDrivingCameraChoiceText = QtWidgets.QLabel(self)
        self.labelDrivingCameraChoiceText.setText("Camera Status : ")
        self.labelDrivingCameraChoiceText.move(670, 130)
        self.labelDrivingCameraChoiceText.resize(80, 20)
        self.labelDrivingCameraChoiceText.setEnabled(False)

        self.labelDrivingCameraChoiceValue = QtWidgets.QLabel(self)
        self.labelDrivingCameraChoiceValue.setText("None")
        self.labelDrivingCameraChoiceValue.move(760, 130)
        self.labelDrivingCameraChoiceValue.resize(80, 20)
        self.labelDrivingCameraChoiceValue.setEnabled(False)

        self.buttonExecute = QtWidgets.QPushButton(self)
        self.buttonExecute.setText("START!")
        self.buttonExecute.move(0, 175)
        self.buttonExecute.resize(900, 50)
        self.buttonExecute.clicked.connect(self.execute)

    def gettingImageName(self):
        self.imageName = QFileDialog.getOpenFileName()[0]

    def gettingVideoName(self):
        self.videoName = QFileDialog.getOpenFileName()[0]

    def imageVideoProcessingButtonClicked(self):
        self.labelImageName.setEnabled(True)
        self.labelVideoName.setEnabled(True)
        self.buttonImageName.setEnabled(True)
        self.buttonVideoName.setEnabled(True)
        self.labelSimulationCameraText.setEnabled(False)
        self.labelSimulationCameraChoiceText.setEnabled(False)
        self.labelSimulationCameraChoiceValue.setEnabled(False)
        self.buttonSimulationMainCamera.setEnabled(False)
        self.buttonSimulationSideCamera.setEnabled(False)
        self.labelDrivingCameraText.setEnabled(False)
        self.labelDrivingCameraChoiceText.setEnabled(False)
        self.labelDrivingCameraChoiceValue.setEnabled(False)
        self.buttonDrivingMainCamera.setEnabled(False)
        self.buttonDrivingSideCamera.setEnabled(False)
        self.isImageVideoProcessingEnable = True
        self.isSimulationProcessingEnable = False
        self.isDrivingProcessingEnable = False

    def simulationProcessingButtonClicked(self):
        self.labelImageName.setEnabled(False)
        self.labelVideoName.setEnabled(False)
        self.buttonImageName.setEnabled(False)
        self.buttonVideoName.setEnabled(False)
        self.labelSimulationCameraText.setEnabled(True)
        self.labelSimulationCameraChoiceText.setEnabled(True)
        self.labelSimulationCameraChoiceValue.setEnabled(True)
        self.buttonSimulationMainCamera.setEnabled(True)
        self.buttonSimulationSideCamera.setEnabled(True)
        self.labelDrivingCameraText.setEnabled(False)
        self.labelDrivingCameraChoiceText.setEnabled(False)
        self.labelDrivingCameraChoiceValue.setEnabled(False)
        self.buttonDrivingMainCamera.setEnabled(False)
        self.buttonDrivingSideCamera.setEnabled(False)
        self.isImageVideoProcessingEnable = False
        self.isSimulationProcessingEnable = True
        self.isDrivingProcessingEnable = False
    
    def drivingProcessingButtonClicked(self):
        self.labelImageName.setEnabled(False)
        self.labelVideoName.setEnabled(False)
        self.buttonImageName.setEnabled(False)
        self.buttonVideoName.setEnabled(False)
        self.labelSimulationCameraText.setEnabled(False)
        self.labelSimulationCameraChoiceText.setEnabled(False)
        self.labelSimulationCameraChoiceValue.setEnabled(False)
        self.buttonSimulationMainCamera.setEnabled(False)
        self.buttonSimulationSideCamera.setEnabled(False)
        self.labelDrivingCameraText.setEnabled(True)
        self.labelDrivingCameraChoiceText.setEnabled(True)
        self.labelDrivingCameraChoiceValue.setEnabled(True)
        self.buttonDrivingMainCamera.setEnabled(True)
        self.buttonDrivingSideCamera.setEnabled(True)
        self.isImageVideoProcessingEnable = False
        self.isSimulationProcessingEnable = False
        self.isDrivingProcessingEnable = True    

    def settingMainCamera(self):
        self.mainCamera = True
        self.sideCamera = False
        if self.isSimulationProcessingEnable:
            self.labelSimulationCameraChoiceValue.setText("Main Camera")
        elif self.isDrivingProcessingEnable:
            self.labelDrivingCameraChoiceValue.setText("Main Camera")

    def settingSideCamera(self):
        self.mainCamera = False
        self.sideCamera = True
        if self.isSimulationProcessingEnable:
            self.labelSimulationCameraChoiceValue.setText("Side Camera")
        elif self.isDrivingProcessingEnable:
            self.labelDrivingCameraChoiceValue.setText("Side Camera")

    def execute(self):
        if self.isImageVideoProcessingEnable:
            imageProcessing = ImageProcessing(self.imageName)
            imageProcessing.displayingScreen(self.imageName, imageProcessing.imageFunction())
            videoProcessing = VideoProcessing(self.videoName)
            videoProcessing.videoFunction()

        elif self.isSimulationProcessingEnable:
            if self.mainCamera:
                simulationProcessing = SimulationProcessing(225, 207, 1400, 900, "MainCamera", 1160, 240, 1465, 390)
                simulationProcessing.simulationFunction()
            elif self.sideCamera:
                simulationProcessing = SimulationProcessing(77, 140, 460, 355, "SideCamera",1072, 140, 1455, 355)
                simulationProcessing.simulationFunction()
            else:
                print("Choose Camera!!!")

        elif self.isDrivingProcessingEnable:
            if self.mainCamera:
                drivingProcessing = DrivingProcessing(1280, 720, "MainCamera")
                drivingProcessing.drivingFunction()
            elif self.sideCamera:
                drivingProcessing = DrivingProcessing(1280, 720, "SideCamera")
                drivingProcessing.drivingFunction()
            else:
                print("Choose Camera!!!")

app = QApplication(sys.argv)
win = GUI(100, 100, 900, 225, "Autonomous Car")
win.show()
sys.exit(app.exec_())
"""
while(True):
    print("What do you want to do? (Image & Video Processing: 1, Simulation Processing: 2, Driving: 3, Exit: 0)")
    decision = int(input())
    if decision == 1:
        imageName = "RoadPhotoWithSign.png"
        videoName = "RoadVideo_Trim1.mp4"
        imageProcessing = ImageProcessing(imageName)
        imageProcessing.displayingScreen(imageName, imageProcessing.imageFunction())
        videoProcessing = VideoProcessing(videoName)
        videoProcessing.videoFunction()
    elif decision == 2:
        print("Which camera do you use in the simulation (Main Camera:1, Side Camera: 2, Exit:0)")
        camera = int(input())
        if camera == 1:
            simulationProcessing = SimulationProcessing("MainCamera")
        elif camera == 2:
            simulationProcessing = SimulationProcessing("SideCamera")
        elif camera == 0:
            break
        else:
            print("Wrong input!")
            break
        simulationProcessing.simulationFunction()
    elif decision == 3:
        print("Which camera do you use in the driving? (Main Camera:1, Side Camera: 2, Exit:0)")
        camera = int(input())
        if camera == 1:
            drivingProcessing = DrivingProcessing(1280, 720, "MainCamera")
        elif camera == 2:
            drivingProcessing = DrivingProcessing(1280, 720, "SideCamera")
        elif camera == 0:
            break
        else:
            print("Wrong Input!")
            break
        drivingProcessing.drivingFunction()
    elif decision == 0:
        break
    else:
        print("Wrong input !!")
