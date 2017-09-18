import time
import RPi.GPIO as GPIO  # always needed with RPi.GPIO


class Robot:
    def __init__(self):
        # choose BCM or BOARD numbering schemes. I use BCM
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup() 
        forward_pin = 4
        backward_pin = 17
        left_pin = 22
        right_pin = 27
        self.forward_voltage = 0
        self.backward_voltage = 0
        self.left_voltage = 0
        self.right_voltage = 0

        # set GPIO 25 as output for forward led
        GPIO.setup(forward_pin, GPIO.OUT)
        GPIO.setup(backward_pin, GPIO.OUT)
        GPIO.setup(left_pin, GPIO.OUT)
        GPIO.setup(right_pin, GPIO.OUT)

        # create object forward for PWM on port 25 at 100 Hertz
        self.forward = GPIO.PWM(forward_pin, 100)
        self.backward = GPIO.PWM(backward_pin, 100)
        self.left = GPIO.PWM(left_pin, 100)
        self.right = GPIO.PWM(right_pin, 100)

        # start forward led on 0 percent duty cycle (off)
        self.forward.start(0)
        self.backward.start(0)
        self.left.start(0)
        self.right.start(0)

        self.forward.ChangeDutyCycle(100) 
    
    def stop(self):
        self.backward.ChangeDutyCycle(0)
        self.forward.ChangeDutyCycle(0)
        self.forwardVoltage = 0
        self.backwardVoltage = 0
        
    def go_forward(self, val):
        if self.backward_voltage > 0:
            self.backward.ChangeDutyCycle(0)
        if self.forward_voltage > 0:
            self.forward.ChangeDutyCycle(val)
        else:
            self.forward.ChangeDutyCycle(val)
        self.forward_voltage = val
        self.backward_voltage = 0

    def go_backward(self, val):
        if self.forward_voltage > 0:
            self.forward.ChangeDutyCycle(0)
        if self.backward_voltage > 0:
            self.backward.ChangeDutyCycle(val)
        else:
            self.backward.ChangeDutyCycle(val)
        self.backward_voltage = val
        self.forward_voltage = 0
        
    def turn_right(self):
        if self.left_voltage > 0:
            self.left.ChangeDutyCycle(0)
        if self.right_voltage > 0:
            self.right.ChangeDutyCycle(100)
        else:
            self.right.ChangeDutyCycle(100)
        time.sleep(0.1)
        self.right.ChangeDutyCycle(15)
        self.right_voltage = 15
        self.left_voltage = 0
        
    def turn_left(self):
        if self.right_voltage > 0:
            self.right.ChangeDutyCycle(0)
        if self.left_voltage > 0:
            self.left.ChangeDutyCycle(100)
        else:
            self.left.ChangeDutyCycle(100)
        time.sleep(0.1)
        self.left.ChangeDutyCycle(15)
        self.left_voltage = 15
        self.right_voltage = 0
        
    def straight(self):
        if self.left_voltage > 0:
            self.left.ChangeDutyCycle(0)
            self.right.ChangeDutyCycle(15)
            time.sleep(0.1)

        elif self.right_voltage > 0:
            self.right.ChangeDutyCycle(0)
            self.left.ChangeDutyCycle(15)
            time.sleep(0.1)

        if self.left_voltage > 0:
            self.left.ChangeDutyCycle(0)

        if self.right_voltage > 0:
            self.right.ChangeDutyCycle(0)

        self.left_voltage = 0
        self.right_voltage = 0
        
    def endSession(self):        
        GPIO.cleanup()
        
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
