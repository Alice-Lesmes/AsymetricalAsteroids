import pygame
import os
import random
from constants import *
from network import Network
from ships import *
from projectile import *
from o2 import *
from light import *




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
    
    # This initialises the network class so that it can act as a client
    n = Network()
    # Get the data from the server that's useless
    useless = n.connect()
    p1 = Player(200, 200, 40, 60, (0,0,255))
    enemies = []
    level = 1  # what stage we are on
    wave_length = 5  # how many enemies will spawn

    # I am hopefully gonna move this out of main
    bullet_cycle = 0
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

        # The data from the p2 client
        ship_system_data = n.send(useless)
        shoot_counter += 1
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
                    # decrease
                    print("decrease pressed")
                    light.decrease_scale(LIGHT_SCALE)
                    light.update_light()
                
                if event.key == pygame.K_0:
                    # increase
                    print("decrease pressed")
                    light.increase_scale(LIGHT_SCALE)
                    light.update_light()
                
                if event.key == pygame.K_8:
                    if bullet_cycle == 3:
                        bullet_cycle = 0
                    else:
                        bullet_cycle += 1

                    p1.change_bullet(BULLET_TYPES[bullet_cycle])

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
                    # boss check
                    if str(enemy) == "BOSS" and bullet.damages_player():
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
