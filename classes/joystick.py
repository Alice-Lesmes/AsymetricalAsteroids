from classes.constants import *
import pyfirmata
import time

class Joystick():
    def __init__(self, ship: "Ship"):
        # initialise the joystick
        self.board = pyfirmata.Arduino(DEV_PORT)
        self.ship = ship

        self.it = pyfirmata.util.Iterator(self.board)
        self.it.start()

        # write to selector
        self.board.digital[SELECTOR_PORT].write(1)
        
        self.y_input = self.board.get_pin(ANALOG_Y)
        self.x_input = self.board.get_pin(ANALOG_X)
    
    def print(self):
        x_value = self.x_input.read()
        y_value = self.y_input.read()
        print(f"X: {x_value}, Y: {y_value}")
    
    def move(self):
        # do nothing if we're between 0.45 to 0.55
        # else we apply movement
        x_value = self.x_input.read()
        y_value = self.y_input.read()
        
        if x_value is None or y_value is None:
            return
        
        if x_value < 0.4:
            print(f"passing negative with {x_value}")
            # negative movement
            
            # 0 should have the higher speed, 0.4 having the lowest
            # calculate the multiplier by inversing the value
            # this has a speed multiplier range of 0.25 to 1
            
            # for some reason the joystick is jammed by 0.002
            x_value += 1/OFFSET_VALUE  # avoid zero division error
            x_value = -(1/(x_value*OFFSET_VALUE))
            self.ship.joystickMoveX(x_value)

        elif x_value > 0.6:
            print(f"passing positive movement with {x_value}")
            # positive movement
            # how do we get this to achieve a multiplier range of 0.25 to 1?
            # I have no idea
            
            # convert the value so that 0 is now the fastest
            x_value = 1 - x_value
            x_value += 1/OFFSET_VALUE
            x_value = 1/(x_value*OFFSET_VALUE)
            self.ship.joystickMoveX(x_value)

        if y_value < 0.4:
            # positive movement (yes you heard me right)
            y_value += 1/OFFSET_VALUE
            y_value = -(1/(y_value*OFFSET_VALUE))
            self.ship.joystickMoveY(y_value)
        elif y_value > 0.6:
            # negative movement
            print(f"function call in negative with value of {y_value}")
            y_value = 1 - y_value
            y_value += 1/OFFSET_VALUE
            y_value = (1/(y_value*OFFSET_VALUE))
            
            self.ship.joystickMoveY(y_value)
            

