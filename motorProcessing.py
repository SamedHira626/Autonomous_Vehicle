import Jetson.GPIO as GPIO
import time

class MotorProcessing:
	def __init__(self, leftPin, rightPin):
		self.leftPin = leftPin
		self.rightPin = rightPin
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.leftPin, GPIO.OUT)
		GPIO.setup(self.rightPin, GPIO.OUT)
		
	def motorFunc(self, rightCase, leftCase):
		if leftCase == True and rightCase == False:
			GPIO.output(self.rightPin, GPIO.LOW)
			GPIO.output(self.leftPin, GPIO.HIGH)
		elif rightCase == True and leftCase == False:
			GPIO.output(self.leftPin, GPIO.LOW)
			GPIO.output(self.rightPin, GPIO.HIGH)
		else:
			GPIO.output(self.rightPin, GPIO.LOW)
			GPIO.output(self.leftPin, GPIO.LOW)
		#GPIO.output(self.rightPin, GPIO.LOW)
		#GPIO.output(self.leftPin, GPIO.LOW)
