import pygame

class Boulder:
    images = []
    weight = 0.05
    maxHP = 70
    hp = 150
    speed = 0.2
    y_momentum = 0
    movement = [0,0]
    angle = 0
    tiles = []
    collisions = []

    def __init__(self,pos,move):
        pygame.init()
        self.pos = pos
        self.move_dir = move
        self.images.append(pygame.transform.scale(pygame.image.load('images/boulder_0.png'),(48,48)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/boulder_1.png'),(48,48)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/boulder_2.png'),(48,48)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/boulder_3.png'),(48,48)))
        self.state = 0
        self.rect = pygame.Rect(pos[0],pos[1],self.images[self.state].get_width(),self.images[self.state].get_height())

    def collision_test(self,rect):
        hit_list = []
        for tile in self.tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def translate(self,mov):
        self.collisions = self.move(mov)
        self.pos = [self.rect.x + (self.images[self.state].get_width()/2),self.rect.y + (self.images[self.state].get_height()/2)]
        self.rect.x = self.pos[0] - (self.images[self.state].get_width()/2)
        self.rect.y = self.pos[1] - (self.images[self.state].get_height()/2)

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

    def set_tiles(self,tiles):
        self.tiles = tiles

    def update(self,dt):
        if self.hp >= self.maxHP:
            self.state = 0
        elif self.hp >= 3*(self.maxHP/4):
            self.state = 1
        elif self.hp >= 2*(self.maxHP/4):
            self.state = 2
        elif self.hp >= (self.maxHP/4):
            self.state = 3

        self.angle += 2.25 *dt * -self.move_dir
        if(self.angle >= 360):
            self.angle = 360 - self.angle
        self.movement = [0,0]

        self.y_momentum += self.weight
        if(self.y_momentum > 10):
            self.y_momentum = 10

        if(self.move_dir < 0):
            self.movement[0] += -self.speed * dt * 2
        else :
            self.movement[0] += self.speed * dt * 4
        self.movement[1] += self.y_momentum

        self.translate(self.movement)
        if self.collisions['bottom']:
            self.y_momentum = 0
        if self.collisions['top']:
            self.y_momentum = 0
        if self.collisions['right'] or self.collisions['left']:
            self.move_dir = 0 - self.move_dir

    def render(self,display,scroll):
        self.img_copy = pygame.transform.rotate(self.images[self.state].copy(),self.angle)
        display.blit(self.img_copy,(self.pos[0] - self.img_copy.get_width()/2 - scroll[0],self.pos[1] - self.img_copy.get_height()/2 - scroll[1]))
