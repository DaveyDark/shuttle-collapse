import pygame,random

class Bullet:
    speed = 10
    time = 0.75
    damage = 2
    destroy = False

    def __init__(self,pos,dir,damage,speed,time,spread):
        self.pos = pos
        self.spread = (random.random() - 0.5)*spread
        self.image = pygame.image.load('images/bullet.png')
        self.rect = pygame.Rect(pos[0],pos[1],self.image.get_width(),self.image.get_height())
        self.damage = damage
        self.speed = speed * dir
        self.time = time

    def update(self,dt,boulders,tiles):
        self.time -= dt/60
        self.rect.x += self.speed
        self.rect.y += self.spread*self.speed
        for boulder in boulders:
            if(self.rect.colliderect(boulder.rect)):
                boulder.hp -= self.damage
                self.destroy = True
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.destroy = True
        
        self.pos[0] = self.rect.x
        self.pos[1] = self.rect.y

    def render(self,display,scroll):
        display.blit(self.image,(self.pos[0] - scroll[0],self.pos[1] - scroll[1]))