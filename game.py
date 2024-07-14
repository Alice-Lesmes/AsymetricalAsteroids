import pygame
import os
import random
from constants import *
# from network import *


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
    
    def get_position(self) -> tuple[int]:
        return (self._x, self._y)

    def add_x(self, value: int):
        self._x += value

    def add_y(self, value: int):
        self._y += value

    def change_hor_vel(self):
        """Chnage the direction in which the ship goes"""
        self._hor_vel *= -1


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

    def change_engine_power(self, value: int) -> None:
        """Change the engine power (horizontal velocity)
        
        value should only be 0, 1, 2"""
        if value in [0, 1, 2]:
            self._vel = ENGINE_POWER[value]
            print(f"new engine power is {self._vel}")

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
            bullets.append(Rocket(self._x + self._width//2,
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
        # possibility to change colour
        # if random.randint(1, 75) == 50:
            
        if self.shoot_counter == 30:
            bullets.append(Asteroid(self._x + self._width//2,
                                      self._y + self._height//2,
                                      True,
                                      "Red",
                                      1,
                                      "Red"))
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
        WIN.blit(self.projectile_img, (self.get_x() - 20, self.get_y() - 40))

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

# drawn from https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
class Oxygen():
    def __init__(self, counter: int):
        """
        Parameters:
            counter: the counter
        """
        self.activated = False
        self.limit = 10
        self.counter, self.text = counter, str(counter).ljust(3)

    def start(self):
        """Start the timer"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_1]:
            pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    def stop(self):
        """Stop the timer (and reset the count?)"""
        pygame.time.set_timer(pygame.USEREVENT, 0)
        # track how much time elapses????
        if self.counter <= self.limit:
            self.counter += 1

    def terminate(self):
        if self.counter == 0:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            self.text = "You are dead"

    def count(self):
        self.counter -= 1
        self.text = str(self.counter).ljust(3)
        # print(f"current state of counter is {self.counter}")
    
    def get_count(self):
        return self.counter

    def get_text(self):
        # print(f"get text passing with {self.text}")
        return self.text


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


# will need to modify the function to draw other players???
def redrawWindow(win, player: Player, enemies: list[int], bullets: list[int],
                 level: int, light: "light"):
    # clear the previous box with blank
    win.blit(LEVELS[level].get("bg_image"), (0, 0))

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
    
    # draw shadow
    filter = pygame.surface.Surface((WIDTH, HEIGHT))
    # the less "grey" the colour actually is, the darker the environment
    filter.fill(pygame.color.Color(250, 250, 250))
    # positions break on init
    positions = player.get_position()
    # modify it so that the image centers with the middle of the ship
    new_position = (positions[0] - light.get_img().get_width()//2,
                    positions[1] - light.get_img().get_height()//2)
    filter.blit(light.get_img(), new_position)
    win.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    # update window
    pygame.display.flip()
    pygame.display.update()


def has_collided(ent1, ent2):
    '''
    ent1 = one of the entities involved in the collision
    ent2 = the other entity
    '''
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
    enemies = []
    level = 1  # what stage we are on
    wave_length = 5  # how many enemies will spawn

    # I am hopefully gonna move this out of main
    engine_cycle = 0
    bullet_cycle = 0
    light_cycle = 0
    bullets = []  # store all current bullets

    # temporary constants used to define the game window
    # used to pop bullets that are outside of the game window
    MIN_BORDER = 0
    MAX_BORDER = 500

    # lost logic
    lost = False
    
    #  initialise external modules that are controlled by phone
    shipOxygen = Oxygen(10)
    light = Light()
    
    shoot_counter = 0

    while running:
        shoot_counter += 1
        # p2 = n.send(p1)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            # starts the timer
            shipOxygen.start()

        if keys[pygame.K_2]:
            shipOxygen.stop()

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for oxygen event
            if event.type == pygame.USEREVENT:
                shipOxygen.count()
                shipOxygen.terminate()  # only stops the timer when it reaches 0
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:
                    if light_cycle == 2:
                        light_cycle = 0
                    else:
                        light_cycle += 1

                    light.update_light(light_cycle)
                
                if event.key == pygame.K_8:
                    if bullet_cycle == 3:
                        bullet_cycle = 0
                    else:
                        bullet_cycle += 1

                    p1.change_bullet(BULLET_TYPES[bullet_cycle])
                
                if event.key == pygame.K_7:
                    if engine_cycle == 2:
                        engine_cycle = 0
                    else:
                        engine_cycle += 1
                    
                    p1.change_engine_power(engine_cycle)
                    

            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        # listen for loss
        if shipOxygen.get_count() == 0:
            lost = True

        # generate enemies
        # make sure enemies get killed when they reach the bottom???
        if len(enemies) == 0:
            if level < len(LEVELS):
                level += 1

            wave_length = LEVELS[level].get("enemies")
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
            
            # level 3
            if level == 2:
                boss = Boss(WIDTH//2, -1500, 40, 40, (255, 0, 0), 1000)
                enemies.append(boss)
                print("the boss has spawned")

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
            # remove upon reaching the bottom
            if enemy.get_y() > HEIGHT + 100:
                enemies.remove(enemy)

            enemy.shoot(bullets)
            for bullet in bullets:
                # this needs to be health reduction rather than immediate
                # removal
                if has_collided(enemy, bullet):
                    # dont damage enemies if it is their own weaponry
                    if bullet.damages_player():
                        continue

                    if enemy in enemies:
                        enemy.damage_self(bullet)
                        # print("enemy has been damaged with health " +
                        #       f"{enemy.get_health()}")
                        if not enemy.alive():
                            enemies.remove(enemy)
                    
                    # remove the bullet
                    bullets.pop(bullets.index(bullet))

            if has_collided(enemy, p1):
                p1._health -= 10
                if enemy in enemies:
                    enemies.remove(enemy)

            if random.randint(1, 75) == 50:
                enemy.change_hor_vel()

        # redraw window
        redrawWindow(win, p1, enemies, bullets, level, light)

        # oxygen redraw (I have no idea if this even passes right)
        win.blit(font.render(shipOxygen.get_text(), True, (255, 255, 255)),
                 (32, 48))
        
        # I have no idea what this does but it makes the text appear
        # pygame.display.flip()
        
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
