import pygame
import os
import platform
import random


# these should be moved to constants
WIDTH = 500
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

root = "assets"

if platform.system() != "Windows":
    root = "../assets"

YELLOW_LASER = pygame.image.load(os.path.join(root, "pixel_laser_yellow.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join(root, "pixel_ship_yellow.png"))
ENEMY_SPACE_SHIP = pygame.image.load(os.path.join(root, "enemy_yellow.png"))

SHOOTER_SPACE_SHIP = pygame.image.load(os.path.join(root, "enemy_blue.png"))
PROJECTILE_BLUE = pygame.image.load(os.path.join(root, "pixel_laser_blue.png"))
PROJECTILE_GREEN = pygame.image.load(os.path.join(root, "pixel_laser_green.png"))



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
        self._hor_vel = 3
        self._bullets = []

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def add_x(self, value: int):
        self._x += value

    def add_y(self, value: int):
        self._y += value

    def change_hor_vel(self):
        self._hor_vel *= -1


class Player(Ship):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=100) -> None:
        super().__init__(x, y, width, height, colour, health)
        self.ship_img = YELLOW_SPACE_SHIP   # placeholder
        self.hitbox = pygame.mask.from_surface(self.ship_img)

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
            # at the moment it just shoots from the middle
            bullets.append(Projectile(self._x + self._width//2,
                                      self._y + 10,
                                      False,
                                      "green",
                                      -1,
                                      "normal"))

    def move_bullet(self):
        """I have no idea what I am doing"""
        pass


class Enemy(Ship):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=100) -> None:
        super().__init__(x, y, width, height, colour, health)

    def move(self):
        """Move the enemy downwards"""
        self._y += self._vel
        if self._x <= 10:
            self.change_hor_vel()
        elif self._x >= 450:
            self.change_hor_vel()
        self._x += self._hor_vel

class Basic(Enemy):
    def __init__(self, x: int, y: int, width: int, height: int, colour: str,
                 health=100) -> None:
        super().__init__(x, y, width, height, colour, health)
        self.ship_img = ENEMY_SPACE_SHIP   # placeholder
        self.hitbox = pygame.mask.from_surface(self.ship_img)
    
    def draw(self, win, img=ENEMY_SPACE_SHIP):
        """Draw the enemy

        Parameters:
            win: pygame window
            img: image mask of the enemy
        """
        self.move()

        # hitbox has not been masked
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
                                      "normal"))
            self.shoot_counter = 1
        else:
            self.shoot_counter += 1

    

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

        self.projectile_img = PROJECTILE_GREEN   # placeholder
        self.hitbox = pygame.mask.from_surface(self.projectile_img)

        self._x = x
        self._y = y
        self._damages_player = damages_player
        self._colour = colour
        self._facing = facing
        self._element = element
        self._damage = damage

        self._vel = facing * 12  # facing specifies positive or negative

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

    def get_vel(self):
        return self._vel

    def draw(self, win):
        if self._colour == "blue":
            WIN.blit(PROJECTILE_BLUE, (self.get_x() - 20, self.get_y() - 40))
        elif self._colour == "green":
            WIN.blit(PROJECTILE_GREEN, (self.get_x() - 20, self.get_y() - 40))
        #pygame.draw.circle(win, self._colour, (self._x, self._y), self._radius)

# drawn from https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
class Oxygen():
    def __init__(self, counter: int):
        """
        Parameters:
            counter: the counter
        """
        self.activated = False
        self.counter, self.text = counter, str(counter).ljust(3)

    def start(self):
        """Start the timer"""
        pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    def stop(self):
        """Stop the timer (and reset the count?)"""
        if self.counter == 0:
            pygame.time.set_timer(pygame.USEREVENT, 0)

    def count(self):
        self.counter -= 1
        self.text = str(self.counter).ljust(3)
        # print(f"current state of counter is {self.counter}")
    
    def get_count(self):
        return self.counter

    def get_text(self):
        # print(f"get text passing with {self.text}")
        return self.text


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

    # test size for images
    # enemies are 50x50
    # rockets are 20x80
    # asteroids are 70 x 70
    # pygame.draw.rect(win, (255, 0, 0), (50, 50, 60, 50))

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

    # lost logic
    lost = False
    
    #  initialise external modules that are controlled by phone
    shipOxygen = Oxygen(10)
    # starts the timer
    shipOxygen.start()

    shoot_counter = 0

    while running:
        shoot_counter += 1
        # p2 = n.send(p1)

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for oxygen event
            if event.type == pygame.USEREVENT:
                shipOxygen.count()
                shipOxygen.stop()  # only stops the timer when it reaches 0

            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        # listen for loss
        if shipOxygen.get_count() == 0:
            lost = True

        # generate enemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                # enemies are just generated wayyyyyyy off screen above
                if random.randint(1, 4) == 3: # PLACEHOLDER
                    enemy = Shooter(random.randrange(50, WIDTH-100),
                                random.randrange(-1500, -100),
                                40,
                                40,
                                (255, 0, 0))
                else:
                    enemy = Basic(random.randrange(50, WIDTH-100),
                                random.randrange(-1500, -100),
                                40,
                                40,
                                (255, 0, 0))
                enemies.append(enemy)

        # game logic starts here
        # player movement
        p1.move()

        # bullet logic
        if shoot_counter >= 6:
            p1.shoot(bullets)
            shoot_counter = 0

        for bullet in bullets:
            if has_collided(bullet, p1):
                if bullet.damages_player():
                    p1._health -= 10
                    bullets.remove(bullet)

            # this only shoots horizontally
            # if bullet.get_x() < MAX_BORDER and bullet.get_x() > MIN_BORDER:
            #     bullet.add_x(bullet.get_vel())
            if bullet.get_y() < MAX_BORDER and bullet.get_y() > MIN_BORDER:
                bullet.add_y(bullet.get_vel())
            else:
                # out of bounds
                bullets.pop(bullets.index(bullet))

        for enemy in enemies:
            enemy.shoot(bullets)
            for bullet in bullets:
                if has_collided(enemy, bullet):
                    if enemy in enemies:
                        enemies.remove(enemy)
            if has_collided(enemy, p1):
                p1._health -= 10
                if enemy in enemies:
                    enemies.remove(enemy)
            if random.randint(1, 75) == 50:
                enemy.change_hor_vel()

        # redraw window
        redrawWindow(win, p1, enemies, bullets)

        # oxygen redraw (I have no idea if this even passes right)
        win.blit(font.render(shipOxygen.get_text(), True, (255, 255, 255)),
                 (32, 48))
        
        # I have no idea what this does but it makes the text appear
        pygame.display.flip()
        
        # for some reason setting this to 60 makes the timer less epileptic
        clock.tick(27)


if __name__ == '__main__':
    pygame.init()

    # set font
    font = pygame.font.SysFont('Monospace', 30)
    # set display
    # fixed to use width and height constants
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Bonjour")
    main()
