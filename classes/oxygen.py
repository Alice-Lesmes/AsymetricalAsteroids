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