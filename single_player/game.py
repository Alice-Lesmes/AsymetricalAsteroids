import pygame
import os
import random


# these should be moved to constants
WIDTH = 750
HEIGHT = 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))


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

        self._rect = (self._x, self._y, self._width, self._height)
        self._vel = 5
        self._bullets = []

        self.ship_img = YELLOW_SPACE_SHIP   # placeholder
        self.hitbox = pygame.mask.from_surface(self.ship_img)
    
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def add_x(self, value: int):
        self._x += value

    def add_y(self, value: int):
        self._y += value


class Player(Ship):
    def draw(self, win) -> None:
        WIN.blit(self.ship_img, (self.get_x(), self.get_y()))

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
        if len(bullets) >= 5:
            return

        keys = pygame.key.get_pressed()  # not sure if I should convert to self

        if keys[pygame.K_SPACE]:
            # at the moment it just shoots from the middle
            bullets.append(Projectile(self._x + self._width//2,
                                      self._y + self._height//2,
                                      6,
                                      (0, 0, 255),
                                      -1,
                                      "normal"))

            # I honestly have no idea how to give proper intervals to
            # shooting, it literally shoots it like a beam :skull:
            pygame.time.delay(100)

    def move_bullet(self):
        """I have no idea what I am doing"""
        pass


class Enemy(Ship):
    def draw(self, win):
        """Draw the enemy"""
        self.move()
        WIN.blit(self.ship_img, (self.get_x(), self.get_y()))

    def move(self):
        """Move the enemy downwards"""
        self._y += self._vel


# create projectile class
class Projectile():
    def __init__(self, x: int, y: int, radius: int,
                 colour: tuple[int], facing: int, element: str, damage=100):
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
        self._radius = radius
        self._colour = colour
        self._facing = facing
        self._element = element
        self._damage = damage

        self._vel = facing * 8  # facing specifies positive or negative

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def add_x(self, value: int):
        self._x += value

    def add_y(self, value: int):
        self._y += value

    def get_vel(self):
        return self._vel

    def draw(self, win):
        pygame.draw.circle(win, self._colour, (self._x, self._y), self._radius)


# will need to modify the function to draw other players???
def redrawWindow(win, player: Player, enemies: list[int], bullets: list[int]):
    # clear the previous box with blank
    win.fill((0, 0, 0))

    # draw player
    player.draw(win)
    # p2.draw(win)

    # draw enemies
    for enemy in enemies:
        enemy.draw(win)

    # draw bullets
    for bullet in bullets:
        bullet.draw(win)

    # print(f"current state of bullets is {bullets}")

    # update window
    pygame.display.update()

'''
ent1 = one of the entities involved in the collision
ent2 = the other entity
'''
def has_collided(ent1, ent2):
    offset_x = ent2.get_x() - ent1.get_x()
    offset_y = ent2.get_y() - ent1.get_y()
    return ent1.hitbox.overlap(ent2.hitbox, (offset_x, offset_y)) != None
    # returns True if the entities touch, otherwise returns False

def main():
    # Variable to keep our game loop running
    running = True
    clock = pygame.time.Clock()
    # n = Network()
    # startP = n.get_p()

    p1 = Player(200, 200, 40, 60, (0, 0, 255))
    # enemy1 = Enemy(100, 0, 40, 40, (255, 0, 0))
    enemies = []
    level = 1  # what stage we are on
    wave_length = 5  # how many enemies will spawn
    
    # I am hopefully gonna move this out of main
    bullets = []  # store all current bullets

    # temporary constants used to define the game window
    # used to pop bullets that are outside of the game window
    MIN_BORDER = 0
    MAX_BORDER = 500

    while running:
        clock.tick(27)
        # p2 = n.send(p1)
        # for loop through the event queue
        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        # generate enemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                # enemies are just generated wayyyyyyy off screen above
                enemy = Enemy(random.randrange(50, WIDTH-100),
                              random.randrange(-1500, -100),
                              40,
                              40,
                              (255, 0, 0))
                enemies.append(enemy)

        # game logic starts here
        # player movement
        p1.move()

        # bullet logic
        p1.shoot(bullets)

        for bullet in bullets:
            # this only shoots horizontally
            # if bullet.get_x() < MAX_BORDER and bullet.get_x() > MIN_BORDER:
            #     bullet.add_x(bullet.get_vel())
            if bullet.get_y() < MAX_BORDER and bullet.get_y() > MIN_BORDER:
                bullet.add_y(bullet.get_vel())
            else:
                # out of bounds
                bullets.pop(bullets.index(bullet))

        for enemy in enemies:
            if has_collided(enemy, p1):
                p1._health -= 10
                enemies.remove(enemy)

        # redraw window
        redrawWindow(win, p1, enemies, bullets)


if __name__ == '__main__':
    pygame.init()

    # set display
    win = pygame.display.set_mode((500, 500))

    pygame.display.set_caption("Bonjour")
    main()
