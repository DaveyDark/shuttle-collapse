import pygame

class Background:
    
    def __init__(self,image,scroll_factor,pos,scale):
        self.image = image
        self.scroll_factor = scroll_factor
        self.pos = pos
        self.scale = scale
    
    def render(self,display,scroll):
        display.blit(pygame.transform.scale(self.image,self.scale),(self.pos[0] - scroll[0]*self.scroll_factor,self.pos[1] - scroll[1]*self.scroll_factor))