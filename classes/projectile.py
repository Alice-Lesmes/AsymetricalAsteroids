from classes.constants import *

# create projectile class
class Projectile():
    def __init__(self, x: int, y: int, damages_player: bool,
                 colour, facing: int, element: str, damage=100):
        """
        Parameters:
            x: x position of projectile
            y: y position of projectile
            radius: radius size of the projectile
            colour: projectile colour
            facing: direction (-1 for up, 1 for down)
            element: type of projectile (normal, fire, etc etc)
            damage: how much damage the projectile does (default 100)
        """
        self._x = x
        self._y = y
        self._damages_player = damages_player
        self._colour = colour
        self._facing = facing
        self._element = element
        self._damage = damage

        self._vel = facing * 12  # facing specifies positive or negative
        
        self.set_img()
        self.hitbox = pygame.mask.from_surface(self.projectile_img)
    
    def set_img(self):
        self.projectile_img = BULLET_IMG_DATA.get(self._element)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def add_x(self, value: int):
        self._x += value

    def add_y(self, value: int):
        self._y += value

    def damages_player(self):
        return self._damages_player
    
    def get_damage(self):
        return self._damage

    def get_vel(self):
        return self._vel

    def draw(self, win):
        win.blit(self.projectile_img, (self.get_x() - 20, self.get_y() - 40))

        # OLD
        # if self._colour == "blue":
        #     WIN.blit(PROJECTILE_BLUE, (self.get_x() - 20, self.get_y() - 40))
        # elif self._colour == "green":
        #     WIN.blit(PROJECTILE_GREEN, (self.get_x() - 20, self.get_y() - 40))
        #pygame.draw.circle(win, self._colour, (self._x, self._y), self._radius)


class Asteroid(Projectile):
    def set_img(self):
        self.projectile_img = ASTEROID_IMG_DATA.get(self._element)


class Rocket(Projectile):
    def set_img(self):
        rocket = ROCKET_IMG.copy()
        self.projectile_img = pygame.transform.flip(rocket, False, True)