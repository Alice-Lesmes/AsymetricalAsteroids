import os
import pygame


# Constants

# replace the server address with the local IP
# on windows use ipconfig --all
# on ubuntu use ip a
SERVER_ADDRESS = "192.168.200.169"
SERVER_PORT = 8000

BYTE_SIZE = 2048*2048

# GAME CONSTANTS
WIDTH = 500
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


root = "assets"


YELLOW_LASER = pygame.image.load(os.path.join(root, "pixel_laser_yellow.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join(root, "pixel_ship_yellow.png"))
ENEMY_SPACE_SHIP = pygame.image.load(os.path.join(root, "enemy_yellow.png"))

SHOOTER_SPACE_SHIP = pygame.image.load(os.path.join(root, "enemy_blue.png"))
BOSS_SPACE_SHIP = pygame.image.load(os.path.join(root, "boss.png"))

PROJECTILE_YELLOW = pygame.image.load(os.path.join(root, "pixel_laser_yellow.png"))
PROJECTILE_RED = pygame.image.load(os.path.join(root, "pixel_laser_red.png"))
PROJECTILE_BLUE = pygame.image.load(os.path.join(root, "pixel_laser_blue.png"))
PROJECTILE_GREEN = pygame.image.load(os.path.join(root, "pixel_laser_green.png"))

ASTEROID_RED = pygame.image.load(os.path.join(root, "asteroid_red.png"))
ASTEROID_BLUE = pygame.image.load(os.path.join(root, "asteroid_blue.png"))
ASTEROID_GREEN = pygame.image.load(os.path.join(root, "asteroid_green.png"))

ROCKET_IMG = pygame.image.load(os.path.join(root, "missile.png"))

LEVEL_ONE = {
    "enemies": 5,
    "bg_image": pygame.transform.scale(pygame.image.load(os.path.join(
        root, "background_one.jpg")), (WIDTH, HEIGHT))
}

LEVEL_TWO = {
    "enemies": 10,
    "bg_image": pygame.transform.scale(pygame.image.load(os.path.join(
        root, "background_two.jpg")), (WIDTH, HEIGHT))
}

LEVEL_THREE = {
    "enemies": 15,
    "bg_image": pygame.transform.scale(pygame.image.load(os.path.join(
        root, "background_three.jpg")), (WIDTH, HEIGHT))
}

LEVELS = [LEVEL_ONE, LEVEL_TWO, LEVEL_THREE]


TYPE_ENEMY = "ENEMY"
TYPE_BASIC = "BASIC"
TYPE_SHOOTER = "SHOOTER"
TYPE_BOSS = "BOSS"

# used to adjust how strong the light around the player gets after
# one increase/decrease
START_LIGHT = 15

RADAR_POWER = {
    0: 5,
    1: 15,
    2: 30
}

BULLET_TYPES = [
    "Standard",
    "Fire",
    "Ice",
    "Leaf"
]

BULLET_IMG_DATA = {
    "Standard": PROJECTILE_YELLOW,
    "Fire": PROJECTILE_RED,
    "Ice": PROJECTILE_BLUE,
    "Leaf": PROJECTILE_GREEN
}

STARTER_BULLET = "Standard"

ASTEROID_TYPES = ["Red", "Blue", "Green"]

ASTEROID_IMG_DATA = {
    "Red": ASTEROID_RED,
    "Blue": ASTEROID_BLUE,
    "Green": ASTEROID_GREEN
}

ENGINE_POWER = {
    0: 0,
    1: 7,
    2: 12
}