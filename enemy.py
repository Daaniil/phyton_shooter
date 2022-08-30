from pygame import *
from GameSprite import GameSprite
from random import *

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if  self.rect.y > self.height:
            self.rect.x = randint(80, self.width - 80)
            self.rect.y = 0
            return 1
        return 0