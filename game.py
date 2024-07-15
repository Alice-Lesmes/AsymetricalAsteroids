import pygame
import os.path
import sys
import random

# own imports
from classes.constants import *
from classes.ship import Player, Basic, Shooter, Boss
from classes.oxygen import Oxygen 
from classes.light import Light
from network import *


# will need to modify the function to draw other players???
def redrawWindow(win, player: "Player", enemies: list[int], bullets: list[int],
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

    # load sounds
    # I have to wait for pygame init to actually play the music
    MUSIC = pygame.mixer.music.load(os.path.join(root, "quack_music.mp3"))
    pygame.mixer.music.play(-1)  # loops the music
    
    # why is Sound in caps!!!
    SHOOT_SOUND = pygame.mixer.Sound(os.path.join(root, "blaster.wav"))
    HIT_SOUND = pygame.mixer.Sound(os.path.join(root, "ship_explosion.wav"))

    n = Network()
    # startP = n.get_p()

    p1 = Player(200, 200, 40, 60, (0, 0, 255))
    p1_server_data_resp = n.get_p()
    enemies = []
    level = -1  # what stage we are on
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
        ship_data = n.send(p1_server_data_resp)
        try:
            modules = ship_data['modules']
            # Modules are using capitals for    
            engine_power = ship_data['Engines']
            o2_power = ship_data['O2']

        except:
            if not type(ship_data) is str:
                print(ship_data)
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
                
                if event.key == pygame.K_SPACE:
                    if shoot_counter >= 6:
                        p1.shoot(bullets)
                        SHOOT_SOUND.play()
                        shoot_counter = 0

                    

            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

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

        for bullet in bullets:
            if has_collided(bullet, p1):
                if bullet.damages_player():
                    p1._health -= 10
                    HIT_SOUND.play()
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
                    if enemy.dieoncollision == True:
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

    pygame.display.set_caption("Asymetrical Asteroids")
    main()
