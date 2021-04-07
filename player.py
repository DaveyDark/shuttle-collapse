import pygame,math,bullet
from pygame.locals import *

class Player:
    pygame.init()
    pos = [0,0]
    jumping = False
    tiles = []
    mode = 0
    bullet_damage = 1
    bullet_speed = 10
    bullet_time = 2
    jump_force = -1.75
    speed = 0.75
    bullet_spread = 0.15
    firerate = 1/20
    mag_size = 3
    mag_bullets = 3
    timer = 0
    movement = [0,0]
    y_momentum = 0
    weight = 0.025
    reload_time = 6
    air_timer = 0
    flipped = False
    collisions = []

    def __init__(self,pos):
        self.pos = pos
        self.image = pygame.image.load('anim/player/idle/0.png')
        self.gun_img = pygame.image.load('anim/player/gun.png')
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.image.get_width(),self.image.get_height())
        self.change_mode()

    def change_mode(self):
        if self.mode == 0:
            #switch to burst
            self.mag_size = 3
            self.mag_bullets = 3
            self.bullet_damage = 2
            self.bullet_time = 2
            self.bullet_speed = 18
            self.firerate = 1/20
            self.mode = 1
            self.bullet_spread = 0.075
            self.reload_time = 8
            self.timer = -self.firerate*self.reload_time
        else:
            #switch to full auto
            self.mag_size = 30
            self.bullet_spread = 0.25
            self.mag_bullets = 30
            self.bullet_damage = 2
            self.bullet_time = 0.5
            self.bullet_speed = 10
            self.firerate = 1/10
            self.mode = 0
            self.reload_time = 8
            self.timer = -self.firerate*self.reload_time

    def set_pos(self,new_pos):
        self.pos = new_pos
        self.rect.x = new_pos[0]
        self.rect.y = new_pos[1]

    def collision_test(self,rect):
        hit_list = []
        for tile in self.tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def set_tiles(self,tiles):
        self.tiles = tiles

    def jump(self):
        self.jumping = True

    def move(self,movement):
        coillision_types = {'top' : False , 'left' : False , 'right' : False , 'bottom' : False}
        self.rect.x += movement[0]
        hit_list = self.collision_test(self.rect)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile.left
                coillision_types['right'] = True
            if movement[0] < 0:
                self.rect.left = tile.right
                coillision_types['left'] = True

        self.rect.y += movement[1]
        hit_list = self.collision_test(self.rect)
        for tile in hit_list:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                coillision_types['bottom'] = True
            if movement[1] < 0:
                self.rect.top = tile.bottom
                coillision_types['top'] = True
        return coillision_types

    def translate(self,mov):
        self.collisions = self.move(mov)
        self.pos = [self.rect.x,self.rect.y]

    def flip(self,flipp):
        self.flipped = flipp

    def update(self,dt):
        self.timer += dt/60
        self.air_timer -= 0.25*dt
        self.movement = [0,0]
        if self.jumping:
            if self.air_timer >= 0:
                self.y_momentum += self.jump_force
            self.jumping = False
        self.y_momentum += self.weight
        if self.y_momentum > 300:
            self.y_momentum = 300

        self.movement[1] += self.y_momentum*dt
        self.translate(self.movement)
        if self.collisions['bottom']:
            self.air_timer = 5*dt
            self.y_momentum = 0
        if self.collisions['top']:
            self.y_momentum = 0


    def shoot(self,scroll,display):
        if self.timer < 0:
            return
        self.mx,self.my = pygame.mouse.get_pos()
        self.mag_bullets -= 1
        if(self.mx > display.get_width() /2 + 180):
            self.flipped = False
        else:
            self.flipped = True
        if not self.flipped:
            blt = bullet.Bullet([self.pos[0] + 28,self.pos[1] + 12],1,self.bullet_damage,self.bullet_speed,self.bullet_time,self.bullet_spread)
        else:
            blt = bullet.Bullet([self.pos[0] + 5,self.pos[1] + 12],-1,self.bullet_damage,self.bullet_speed,self.bullet_time,self.bullet_spread)
        self.timer = -self.firerate
        if self.mag_bullets <= 0:
            self.timer -= self.firerate*self.reload_time
            self.mag_bullets = self.mag_size
        return blt

    def can_shoot(self):
        if self.timer < 0:
            return False
        return True

    def render(self,display,scroll):
        display.blit(pygame.transform.flip(self.image,self.flipped,False),(self.pos[0] - scroll[0],self.pos[1] - scroll[1]))
        if not self.flipped:
            display.blit(self.gun_img,(self.pos[0] - scroll[0] + 1,self.pos[1] - scroll[1] + 12))
        else:
            display.blit(pygame.transform.flip(self.gun_img,True,False),(self.pos[0] - scroll[0] - 12,self.pos[1] - scroll[1] + 12))
