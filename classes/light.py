from classes.constants import *

# Initially I only wanted to import START_LIGHT and RADER_POWER but for some
# reason it doesn't work and using a star import fixes everything apparently
# this is adapted from
# https://stackoverflow.com/questions/31038285/python-pygame-game-lighting


class Light():
    """The radar/visibility of the ship."""
    def __init__(self):
        self.light = pygame.image.load(os.path.join(root, 'circle.png'))
        self.scale = START_LIGHT
        self._starter_width = self.light.get_width()
        self._starter_height = self.light.get_height()
        self.size = (self._starter_width * self.scale,
                     self._starter_height * self.scale)
        self.light = pygame.transform.scale(self.light, self.size)
        self._tick = 0

    def update_light(self, value: int) -> None:
        """
        value should only be 0, 1 or 2
        """
        if value in [0, 1, 2]:
            self.scale = RADAR_POWER.get(value)
            self.update_size()
            print(f"update size is {self.size} with scale {self.scale}")
            self.light = pygame.transform.scale(self.light, self.size)
    
    def update_size(self):
        self.size = (self._starter_width * self.scale,
                     self._starter_height * self.scale)
    
    # increase and decrease functions are now deprecated
    def decrease_scale(self, value: int) -> None:
        if self.scale > 0+value:
            self.scale -= value
        self.update_size()
    
    def increase_scale(self, value: int) -> None:
        self.scale += value
        self.update_size()
    
    # find a function to handle 0, 1, 2

    def get_img(self):
        return self.light