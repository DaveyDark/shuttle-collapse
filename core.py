import pygame

class Core:
    hp = 100

    def __init__(self,pos):
        self.image = pygame.transform.scale(pygame.image.load('images/core.png'),(130,100))
        self.pos = pos
        self.rect = pygame.Rect(pos[0]+ 25,pos[1] + 40,self.image.get_width()-45,self.image.get_height()-22)

    def update(self,dt,boulders):
        for boulder in boulders:
            if self.rect.colliderect(boulder.rect):
                self.hp -= 10
                print(self.hp)
                boulder.hp = 0

    def render(self,display,scroll):
        display.blit(self.image,(self.pos[0] - scroll[0],self.pos[1] - scroll[1]))