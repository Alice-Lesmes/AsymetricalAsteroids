from classes.constants import *
import pyfirmata
import time

class Joystick():
    def __init__(self, board, ship: "ship"):
        # initialise the joystick
        self.board = board
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
            x_value = -(1 - x_value)
            self.ship.joystickMoveX(x_value)

        elif x_value > 0.6:
            print(f"passing positive movement with {x_value}")
            # positive movement
            self.ship.joystickMoveX(x_value)

        if y_value < 0.4:
            # negative movement (yes you heard me right)
            y_value = 1 - y_value
            self.ship.joystickMoveY(-y_value)
        elif y_value > 0.6:
            # positive movement
            print(f"function call in negative with value of {y_value}")
            self.ship.joystickMoveY(y_value)
            

class Button():
    def __init__(self, board, ship):
        self.board = board
        self.shoot_input = self.board.get_pin(SHOOT_PIN)
        self.ship = ship
        self._shoot_counter = 7
    
    def shoot(self, bullets, shootSound):
        shoot = self.shoot_input.read()
        if (shoot and self._shoot_counter > 7):
            self.ship.shoot(bullets, shootSound)
            self._shoot_counter = 0
        
        if self._shoot_counter <= 7:
            self._shoot_counter += 1


class Controller():
    def __init__(self, ship):
        self.board = pyfirmata.Arduino(DEV_PORT)
        self.joystick = Joystick(self.board, ship)
        self.button = Button(self.board, ship)

    def move(self):
        self.joystick.move()
    
    def shoot(self, bullets, shootSound):
        self.button.shoot(bullets, shootSound)
