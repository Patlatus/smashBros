import sys
import os
import pygame
from pygame.locals import *

class Character(pygame.sprite.Sprite):
    def __init__(self, game=None):
        #initialize sprite object
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        #create the images
        self.red = pygame.image.load("media/red.png")
        self.blue = pygame.image.load("media/blue.png")
        self.green = pygame.image.load("media/green.png")

        self.image = pygame.image.load("media/mario.png")
        self.rect = self.image.get_rect()

        # Reset variables
        self.startPos = (self.game.width/2, self.game.height/3)
        self.startVel = (0, 0)
        self.startDamage = 0
        self.resetCharacter()

        # General Variables
        self.lives = 3
        self.damage = self.startDamage

        # Character specific variables
        # These will change depening on the character
        self.maxJumps = 2
        self.jumpVelocity = 40

        # Create the physics engine for this character
        self.offLeft = False
        self.offRight = False

        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel

        self.jumpsRemaining = self.maxJumps
        self.isOnGround = False

    def move(self, button):
        """Function to handle movement from input"""
        pass

    def jump(self):
        if self.jumpsRemaining > 0:
            print 'Jumping'
            self.yvel = -1 * self.jumpVelocity
            self.ypos += self.yvel
            self.jumpsRemaining -= 1

    def Aattack(self):
        print 'A attack'

    def Battack(self):
        print 'B attack'

    def mapCollision(self):
        c = self.rect
        m = self.game.platform.rect

        topCollision = leftCollision = rightCollision = False
        above = below = left = right = False

        if c.top > m.bottom: below = True
        if c.bottom < m.top: above = True
        if c.left > m.right: right = True
        if c.right < m.left: left = True
        if above or below or left or right:
            if left:
                self.offLeft = True
                print 'offLeft'
            if right:
                self.offRight = True
                print 'off Right'
            return False # There is no collision
        
        if c.bottom >= m.top and c.top < m.top and self.offRight == False and self.offLeft == False:
            self.jumpsRemaining = self.maxJumps
            self.ypos = m.top - c.height/2
            self.yvel = 0
            topCollision = True

        if c.left <= m.right and c.right > m.left and topCollision == False:
            print 'Right collide'
            rightCollision = True

        if c.right >= m.left and c.left > m.right and topCollision == False:
            print 'Left collide'
            leftCollision = True

    def gravity(self):
        #Apply gravity
        gravity = 5
        if not self.mapCollision():
            self.yvel += gravity
            self.ypos += self.yvel
        
    def checkDeath(self):
        """Chacks if a user is dead or not"""
        if not self.game.screenRect.contains(self.rect):
            print 'Death'
            self.lives -= 1
            if self.lives < 1:
                sys.exit()
            self.resetCharacter()

    def resetCharacter(self):
        """Resets the character to the starting spot"""
        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel
        self.rect.center = (self.xpos, self.ypos)
        self.damage = self.startDamage
        
    def moveRight(self, right):
        if right == True:
            self.xpos += 10
        else:
            self.xpos -= 10

    def tick(self):
        #Get the right/left movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            pass
        elif keys[K_LEFT]:
            self.moveRight(False)
        elif keys[K_RIGHT]:
            self.moveRight(True)

        self.gravity()

        #Get the attacks/jumping movement
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #If this is true, jump
                if event.key == pygame.K_SPACE:
                    self.jump()
                elif event.key == pygame.K_a:
                    self.Aattack()
                elif event.key == pygame.K_s:
                    self.Battack()
                elif event.key == pygame.K_q:
                    sys.exit()
                    
        self.rect.center = (self.xpos, self.ypos)
        self.checkDeath()
            
