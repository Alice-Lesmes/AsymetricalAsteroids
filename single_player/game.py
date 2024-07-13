import pygame


class Player():
    def __init__(self, x: int, y: int, width: int, height: int, colour: str
                 ) -> None:
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
        self._rect = (self._x, self._y, self._width, self._height)
        self._vel = 5

    def draw(self, win) -> None:
        # draw a rectangle (the player)
        pygame.draw.rect(win, self._colour, self._rect)

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
        
        if len(bullets) >= 5:
            return

        keys = pygame.key.get_pressed()  # not sure if I should convert to self
        
        if keys[pygame.K_SPACE]:
            # at the moment it just shoots from the middle 
            bullets.append(Projectile(self._x + self._width//2,
                                      self._y + self._height//2,
                                      6,
                                      (0, 0, 255),
                                      1,
                                      "normal"))
            
            # I honestly have no idea how to give proper intervals to
            # shooting, it literally shoots it like a beam :skull:
            pygame.time.delay(100)

# bullets shoot too fast lmao


# create projectile class
class Projectile():
    def __init__(self, x: int, y: int, radius: int,
                 colour: tuple[int], facing: int, element: str):
        """
        Parameters:
            x: x position of projectile
            y: y position of projectile
            radius: radius size of the projectile
            colour: projectile colour
            facing: direction it is facing in degrees (no clue where 0 faces)
            element: type of projectile (normal, fire, etc etc)
        """
        self._x = x
        self._y = y
        self._radius = radius
        self._colour = colour
        self._facing = facing
        self._vel = facing * 8 # I have no idea what this does
        self._element = element
    
    def get_x(self):
        return self._x
    
    def add_x(self, value: int):
        self._x += value

    def get_vel(self):
        return self._vel
    
    def draw(self, win):
        pygame.draw.circle(win, self._colour, (self._x, self._y), self._radius)


# will need to modify the function to draw other players???
def redrawWindow(win, player, bullets): 
    # clear the previous box with blank
    win.fill((0, 0, 0))
    
    # draw player
    player.draw(win)
    # p2.draw(win)
    
    # draw bullets
    for bullet in bullets:
        bullet.draw(win)
    
    # print(f"current state of bullets is {bullets}")

    # update window
    pygame.display.update()


def main():
    # Variable to keep our game loop running
    running = True
    clock = pygame.time.Clock()
    # n = Network()
    # startP = n.get_p()

    p1 = Player(50, 50, 40, 60, (255, 0, 0))
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

        # game logic starts here
        # player movement
        p1.move()
        
        # bullet logic
        p1.shoot(bullets)

        for bullet in bullets:
            if bullet.get_x() < MAX_BORDER and bullet.get_x() > MIN_BORDER:
                bullet.add_x(bullet.get_vel())
            else:
                # out of bounds
                bullets.pop(bullets.index(bullet))
        
        # redraw window
        redrawWindow(win, p1, bullets)


if __name__ == '__main__':
    pygame.init()

    # set display
    win = pygame.display.set_mode((500, 500))

    pygame.display.set_caption("Bonjour")
    main()
