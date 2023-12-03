import random
import pygame
import main

WHITE = (255, 255, 255)

powerUpKeys = {}

class PowerUp(pygame.sprite.Sprite):
    # This class represents a Power-Up
    # A Power-Up is something a player can “catch” by hitting it with the car. 
    # Catching a “Power-up” will affect the game in some way for a temporary amount of time.
    
    # The available types of power-ups are: Invincibility, Slowing, Repaint, Invisibility and Random
    def __init__(self, type, speed, timeout = 3000):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set the power up image
        self.image = pygame.image.load(f'assets/powerup_{type}.png')

        #Initialise attributes of the sprite.
        self.width = 50
        self.height = 50
        self.speed = speed
        self.type = type
        
        self.startTime = None  # property to use for the timeout of the powerup
        self.timeout = timeout  # 3 seconds timeout default
        self.typeWhenActivated = None  # store what was the type when the power up was last activated
        # we need to do this because the powerup will be reused after colliding with the player
        # and its type can change
        

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def affectPlayer(self, player):
        # Disable the previous power up before setting the new one
        if main.active_power_up:
            main.active_power_up.deactivate(player)
        
            
        powerUpTypes = ("invincibility", "slowing", "repaint", "random", "invisibility")
        
        if self.type == "random":
            self.type = random.choice(powerUpTypes)
        if self.type == "invincibility":
            player.invincible = True
            player.image = pygame.image.load(f'assets/car_invincible.png')
        elif self.type == "slowing":
            main.speed = 0.2
            player.image = pygame.image.load(f'assets/car_slowing.png')
        elif self.type == "repaint":
            player.repaint(isPlayer=True)
        elif self.type == "invisibility":
            player.setInvisible()
        
        # Store the active power up
        main.active_power_up = self
        self.startTime = pygame.time.get_ticks()
        self.typeWhenActivated = self.type
    
    def deactivate(self, player):
        print("deactivate power up")
        
        if self.typeWhenActivated == "invincibility":
            player.invincible = False
            player.image = pygame.image.load(f'assets/car{main.selected_car}.png')
        elif self.typeWhenActivated == "slowing":
            main.speed = 1
            player.image = pygame.image.load(f'assets/car{main.selected_car}.png')
        elif self.typeWhenActivated == "repaint":
            pass
        elif self.typeWhenActivated == "invisibility":
            player.setVisible()
        
        main.active_power_up = None
        self.startTime = None
        self.typeWhenActivated = None

    def moveForward(self, speed):
        self.rect.y += speed * 2

    def moveBackward(self, speed):
        self.rect.y -= speed * 2

    def changeSpeed(self, speed):
        self.speed = speed

    def repaint(self, type):
        self.image = pygame.image.load(f'assets/powerup_{type}.png')
        self.type = type
    
    def create_mask(self):
        return pygame.mask.from_surface(self.image)