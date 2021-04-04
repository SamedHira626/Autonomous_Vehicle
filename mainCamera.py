from imageProcessing import ImageProcessing

class MainCamera:
    def __init__(self, image):
        self.image = image

    def capturingFunction(self):
        imageProcessing.image = self.image
        imageProcessing.showingScreen("Captured Frame", imageProcessing.imageFunction())
        if imageProcessing.slope < -4:
            return False, True, False #F L R
        if imageProcessing.slope > 4:
            return False, False, True #F L R
        if -4 <= imageProcessing.slope <= 4:
            return True, False, False #F L R

imageProcessing = ImageProcessing()