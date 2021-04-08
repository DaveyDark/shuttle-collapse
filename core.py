import pygame

class Core:
    hp = 50

    def __init__(self,pos):
        self.image = pygame.transform.scale(pygame.image.load('images/core.png'),(130,100))
        self.pos = pos
        self.rect = pygame.Rect(pos[0]+ 25,pos[1] + 40,self.image.get_width()-45,self.image.get_height()-22)

    def update(self,dt,boulders,sound):
        for boulder in boulders:
            if self.rect.colliderect(boulder.rect):
                self.hp -= 10
                sound.play()
                print(self.hp)
                boulder.hp = -1000

    def render(self,display,scroll):
        display.blit(self.image,(self.pos[0] - scroll[0],self.pos[1] - scroll[1]))