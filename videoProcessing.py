import time
import cv2
from imageProcessing import ImageProcessing

class VideoProcessing:
    def __init__(self, videoName):
        self.videoName = videoName
        self.frameCounter = 0
        self.second = 0
        
    def videoFunction(self):
        cap = cv2.VideoCapture(self.videoName)
        first = time.time()
        while(cap.isOpened()):
            _, frame = cap.read()
            if frame is not None:
                imageProcessing.image = frame
                cv2.imshow(self.videoName, imageProcessing.imageFunction())
                last = time.time() - first
                if 0.95 < last < 1.01:
                    self.second += 1
                    print(self.second, "second(s),", "FPS:", self.frameCounter)
                    self.frameCounter = 0
                    first = time.time()
                self.frameCounter = self.frameCounter + 1           
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("The video is finished.")
                cap.release()
                cv2.destroyAllWindows()

imageProcessing = ImageProcessing()