import time
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
class Robot:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
        GPIO.cleanup() 
        forwardPin = 4
        backwardPin = 17
        leftPin = 22
        rightPin = 27
        self.forwardVoltage = 0
        self.backwardVoltage = 0
        self.leftVoltage = 0
        self.rightVoltage = 0

        GPIO.setup(forwardPin, GPIO.OUT)# set GPIO 25 as output for forward led
        GPIO.setup(backwardPin, GPIO.OUT)
        GPIO.setup(leftPin, GPIO.OUT)
        GPIO.setup(rightPin, GPIO.OUT)
          
        self.forward = GPIO.PWM(forwardPin, 100)    # create object forward for PWM on port 25 at 100 Hertz 
        self.backward = GPIO.PWM(backwardPin, 100)
        self.left = GPIO.PWM(leftPin, 100)
        self.right = GPIO.PWM(rightPin, 100)
          
        self.forward.start(0)
        self.backward.start(0)
        self.left.start(0)
        self.right.start(0)              # start forward led on 0 percent duty cycle (off) 

        self.forward.ChangeDutyCycle(100) 
          
    def goForward(self,val):
        if(self.backwardVoltage > 0):
            self.backward.ChangeDutyCycle(0)
        if(self.forwardVoltage > 0):
            self.forward.ChangeDutyCycle(val)
        else:
            self.forward.ChangeDutyCycle(val)
        self.forwardVoltage = val
        self.backwardVoltage = 0

    def goBackward(self,val):
        if(self.forwardVoltage > 0):
            self.forward.ChangeDutyCycle(0)
        if(self.backwardVoltage > 0):
            self.backward.ChangeDutyCycle(val)
        else:
            self.backward.ChangeDutyCycle(val)
        self.backwardVoltage = val
        self.forwardVoltage = 0
        
    def turnRight(self):
        if(self.leftVoltage > 0):
            self.left.ChangeDutyCycle(0)
        if(self.rightVoltage > 0):
            self.right.ChangeDutyCycle(100)
        else:
            self.right.ChangeDutyCycle(100)
        time.sleep(0.1)
        self.right.ChangeDutyCycle(15)
        self.rightVoltage = 15
        self.leftVoltage = 0
        
    def turnLeft(self):     
        if(self.rightVoltage > 0):
            self.right.ChangeDutyCycle(0)
        if(self.leftVoltage > 0):
            self.left.ChangeDutyCycle(100)
        else:
            self.left.ChangeDutyCycle(100)
        time.sleep(0.1)
        self.left.ChangeDutyCycle(15)
        self.leftVoltage = 15
        self.rightVoltage = 0
        
    def straight(self):
        if(self.leftVoltage > 0):
            self.left.ChangeDutyCycle(0)
            self.right.ChangeDutyCycle(15)
            time.sleep(0.1)
        elif(self.rightVoltage > 0):
            self.right.ChangeDutyCycle(0)
            self.left.ChangeDutyCycle(15)
            time.sleep(0.1)
        if(self.leftVoltage > 0):    
            self.left.ChangeDutyCycle(0)
        if(self.rightVoltage > 0):
            self.right.ChangeDutyCycle(0)
        self.leftVoltage = 0
        self.rightVoltage = 0
        
# robot = Robot()     
# try:
    # while 1:
        # for dc in range(0, 101, 5):
            # robot.goForward(dc)
            # time.sleep(0.1)
        # for dc in range(0, 101, 5):
            # robot.goBackward(dc)
            # time.sleep(0.1)
        # robot.turnLeft()
        # time.sleep(2)
        # robot.straight()
        # time.sleep(2)
        # robot.turnRight()
        # time.sleep(2)
        # robot.turnLeft()
        # time.sleep(2)
        # robot.turnRight()

# except KeyboardInterrupt:
    # pass
GPIO.cleanup()
