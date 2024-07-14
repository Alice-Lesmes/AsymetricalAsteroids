import pygame
from constants import *
# Ships
class Ship():
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=100) -> None:
        """
        Parameters:
            x: initial x position
            y: initial y position
            width: size
            height: size
            colour: colour of player
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._colour = colour
        self._health = health
        self._power = 0

        self._rect = (self._x, self._y, self._width, self._height)
        self._vel = 5
        self._hor_vel = 3 + self._power
        self._bullets = []

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
    
    def get_position(self) -> tuple[int]:
        return (self._x, self._y)

    def add_x(self, value: int):
        self._x += value

    def add_y(self, value: int):
        self._y += value

    def change_hor_vel(self):
        """Chnage the direction in which the ship goes"""
        self._hor_vel *= -1
    
    def change_power(self, value: int):
        """Change power, which is the offset controlled by P2.
        
        Okay tbh I have no idea what this does anymore (Ryan)
        """
        self._power = value


class Player(Ship):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=100) -> None:
        super().__init__(x, y, width, height, colour, health)
        self.ship_img = YELLOW_SPACE_SHIP   # placeholder
        self.hitbox = pygame.mask.from_surface(self.ship_img)
        self.bullet_type = STARTER_BULLET

    def draw(self, win) -> None:
        WIN.blit(self.ship_img, (self.get_x(), self.get_y()))
        self.healthbar(win)

    def healthbar(self, win):
        pygame.draw.rect(win, (255,0,0), (self._x, self._y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(win, (0,255,0), (self._x, self._y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self._health/100), 10))

    def move(self) -> None:
        # add key listener
        keys = pygame.key.get_pressed()

        # key handler
        if keys[pygame.K_LEFT]:
            self._x -= self._vel
        if keys[pygame.K_RIGHT]:
            self._x += self._vel
        if keys[pygame.K_UP]:
            self._y -= self._vel
        if keys[pygame.K_DOWN]:
            self._y += self._vel

        self._rect = (self._x, self._y, self._width, self._height)

    def shoot(self, bullets: list[int]) -> None:
        """
        Parameters:
            bullets: list of all bullets in the game
        """
        # this needs to be modified
        if len(bullets) >= 50:
            return

        keys = pygame.key.get_pressed()  # not sure if I should convert to self

        if keys[pygame.K_SPACE]:
            bullets.append(Projectile(self._x + self._width//2,
                                      self._y + 10,
                                      False,
                                      "green",
                                      -1,
                                      self.bullet_type))
            print(f"Player shot bullet with type {self.bullet_type}")

    def change_bullet(self, bullet: str) -> None:
        """Change the bullet type/element"""
        if bullet in BULLET_TYPES:
            self.bullet_type = bullet
            print(f"Bullet type has been changed to {bullet}")

    def get_bullet_type(self):
        """I don't even know if I need this"""
        return self.bullet_type

    def move_bullet(self):
        """I have no idea what I am doing"""
        pass


class Enemy(Ship):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=100) -> None:
        super().__init__(x, y, width, height, colour, health)
    
    def __str__(self):
        return TYPE_ENEMY

    def move(self):
        """Move the enemy downwards"""
        self._y += self._vel
        if self._x <= 10:
            self.change_hor_vel()
        elif self._x >= 450:
            self.change_hor_vel()
        self._x += self._hor_vel
    
    def damage_self(self, projectile: "Projectile") -> None:
        """Damage the enemy"""
        damage = projectile.get_damage()
        print(self.__str__() + f" has taken {damage}")
        self._health -= damage
    
    def alive(self):
        """Returns if the enemy is alive"""
        if self._health > 0:
            return True
        return False

    def get_health(self):
        return self._health


class Basic(Enemy):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=100) -> None:
        super().__init__(x, y, width, height, colour, health)
        self.ship_img = ENEMY_SPACE_SHIP   # placeholder
        self.hitbox = pygame.mask.from_surface(self.ship_img)
    
    def __str__(self):
        return TYPE_BASIC
    
    def draw(self, win, img=ENEMY_SPACE_SHIP):
        """Draw the enemy

        Parameters:
            win: pygame window
            img: image mask of the enemy
        """
        self.move()

        # hitbox has not been masked (wait but it has?)
        WIN.blit(img, (self.get_x(), self.get_y()))

    def shoot(self, bullets):
        # This enemy does not shoot
        return


class Shooter(Enemy):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=100) -> None:
        super().__init__(x, y, width, height, colour, health)
        self.ship_img = SHOOTER_SPACE_SHIP   # placeholder
        self.hitbox = pygame.mask.from_surface(self.ship_img)
        self.shoot_counter = 15
    
    def __str__(self):
        return TYPE_SHOOTER

    def draw(self, win, img=SHOOTER_SPACE_SHIP):
        """Draw the enemy
        
        Parameters:
            win: pygame window
            img: image mask of the enemy
        """
        self.move()

        # hitbox has not been masked
        WIN.blit(img, (self.get_x(), self.get_y()))

    def shoot(self, bullets):  # list of bullets
        if self.shoot_counter == 30:
            bullets.append(Projectile(self._x + self._width//2,
                                      self._y + self._height//2,
                                      True,
                                      "blue",
                                      1,
                                      "Standard"))
            self.shoot_counter = 1
        else:
            self.shoot_counter += 1


class Boss(Enemy):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=2000) -> None:
        super().__init__(x, y, width, height, colour, health)
        # for some reason setting this to BOSS_SPACE_SHIP causes it to disappear
        # so yay???
        self.ship_img = BOSS_SPACE_SHIP   # placeholder
        self.hitbox = pygame.mask.from_surface(self.ship_img)
        self.shoot_counter = 15
        self.max_health = health
        self.start_attack = False
    
    def __str__(self) -> str:
        return TYPE_BOSS

    def draw(self, win, img=BOSS_SPACE_SHIP):
        """Draw the enemy
        
        Parameters:
            win: pygame window
            img: image mask of the enemy
        """
        self.move()
        self.healthbar(win)

        # hitbox has not been masked
        WIN.blit(img, (self.get_x(), self.get_y()))
    
    def healthbar(self, win):
        # red bg
        pygame.draw.rect(win, (255,0,0), (self._x, self._y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        
        # green (actual health)
        # this 10 at the end needs to be changed to smth
        pygame.draw.rect(win, (0,255,0), (self._x, self._y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self._health/self.max_health), 10))

    def shoot(self, bullets):  # list of bullets
        if self.shoot_counter == 30:
            bullets.append(Projectile(self._x + self._width//2,
                                      self._y + self._height//2,
                                      True,
                                      "blue",
                                      1,
                                      "Standard"))
            self.shoot_counter = 1
        else:
            self.shoot_counter += 1
    
    def move(self):
        """Move the enemy downwards"""
        # unless the enemy is at the top
        if self._y < 0:
            self._y += self._vel

        if self._x <= 10:
            self.change_hor_vel()
        elif self._x >= 450:
            self.change_hor_vel()
        self._x += self._hor_vel
    
