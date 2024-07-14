import pygame
from constants import *
# Lights (radar)
class Light():
    def __init__(self):
        self.light = pygame.image.load(os.path.join(root, 'circle.png'))
        self.scale = START_LIGHT
        self._starter_width = self.light.get_width()
        self._starter_height = self.light.get_height()
        self.size = (self._starter_width * self.scale,
                     self._starter_height * self.scale)
        self.light = pygame.transform.scale(self.light, self.size)
        self._tick = 0

    def update_light(self):
        print(f"update size is {self.size} with scale {self.scale}")
        self.light = pygame.transform.scale(self.light, self.size)
    
    def update_size(self):
        self.size = (self._starter_width * self.scale,
                     self._starter_height * self.scale)
    
    def decrease_scale(self, value: int) -> None:
        if self.scale > 0+value:
            self.scale -= value
        self.update_size()
    
    def increase_scale(self, value: int) -> None:
        self.scale += value
        self.update_size()

    def get_img(self):
        return self.light

