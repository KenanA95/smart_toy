# Actual robot.py can only be run on the raspberry PI
# Class for testing purposes only


class Robot:
    def __init__(self):
        pass

    def go_forward(self, val):
        print("ROBOT go forward {0}...".format(val))

    def go_backward(self, val):
        print("ROBOT go backward {0}...".format(val))

    def turn_right(self):
        print("ROBOT turn right")

    def turn_left(self):
        print("ROBOT turn left")

    def go_straight(self):
        print("ROBOT go STRAIGHT")