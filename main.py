import pygame,sys,DarkEngine,time,math,random,core #modules
import player,backgroud,boulder #game files
from pygame.locals import *
from DarkEngine import *

#---------------------------------------constants---------------------------------------
WINDOW_SIZE = (1280,720)
#WINDOW_SIZE = (960,540)
#WINDOW_SIZE = (640,360)
DISPLAY_SIZE = (640,360)

#--------------------------------------PYGAME SETUP---------------------------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface(DISPLAY_SIZE)

#--------------------------------------FILE LOADING---------------------------------------
game_map = load_map('map/map1')
game_map_bg = load_map('map/map1bg')
tileset = [pygame.image.load('images/surface.png').convert(),
           pygame.image.load('images/ground.png').convert()]
bg_tileset = [pygame.image.load('images/spaceshipbg.png').convert()]
boulders = []
bullets = []

#---------------------------------------OBJECTS---------------------------------------
player = player.Player([1060,700])
bg = backgroud.Background(pygame.image.load('images/space.png'),0.1,[-600,-600],(2048,2048))
core = core.Core([1010,655])
spawn_locations = [(464,10),(920,10),(1185,10),(1650,10)]
animation_database = {}
animation_frames = {}
player_action = 'idle'
player_frame = 0
animation_database['idle'] = load_animation('anim/player/idle',[30,30],animation_frames)
animation_database['walk'] = load_animation('anim/player/walk',[4,4,4,4,4,4,4],animation_frames)
animation_database['jump'] = load_animation('anim/player/jump',[20],animation_frames)

#---------------------------------------VARIABLES---------------------------------------
old_time = time.time()
shooting = False
scroll = [0,0]
move = 0
font = pygame.font.Font(None,32)
spawn_rate = [20,40]
spawn_timer = 0
score = 0

#---------------------------------------MORE INIT---------------------------------------
tiles = render_map(game_map,display,tileset,[0,0],['1','2'])
player.set_tiles(tiles)
for bder in boulders:
    bder.set_tiles(tiles)

#---------------------------------------GAME LOOP---------------------------------------
while True:
    display.fill((30,30,30))
    dt,old_time = calc_dt(old_time)

    #---------------------------------------scrolling---------------------------------------
    true_scroll = scroll.copy()
    true_scroll[0] += (player.pos[0] - true_scroll[0] - (display.get_width()/2) - (player.image.get_width()/2))/15
    true_scroll[1] += (player.pos[1] - true_scroll[1] - (display.get_height()/2) - (player.image.get_height()/2))/15
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #---------------------------------------animation handling---------------------------------------
    player_image_id = animation_database[player_action][int(player_frame)]
    player.image = animation_frames[player_image_id]
    player_frame += dt
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0

    #---------------------------------------event handling---------------------------------------
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                player.flip(False)
                move = 1
            if event.key == K_a:
                player.flip(True)
                move = -1
            if event.key == K_w:
                player.jump()
        if event.type == KEYUP:
            if event.key == K_d:
                if move == 1:
                    move = 0
            if event.key == K_a:
                if move == -1:
                    move = 0
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                shooting = True
            if event.button == 3:
                player.change_mode()
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                shooting = False

    if(move != 0):
        player_action,player_frame = change_action(player_action,player_frame,'walk')
    else :
        player_action,player_frame = change_action(player_action,player_frame,'idle')

    if int(player.y_momentum) != 0:
        player_action,player_frame = change_action(player_action,player_frame,'jump')

    #---------------------------------------boulder spawning---------------------------------------
    if(spawn_timer >= 0):
        #spawn boulder
        spawn_timer = -random.randrange(int(spawn_rate[0]),int(spawn_rate[1]))
        spawn_loc = random.randrange(0,4)
        boulders.append(boulder.Boulder(spawn_locations[spawn_loc],1))
    spawn_timer += dt/60

    #---------------------------------------updates---------------------------------------
    spawn_rate[0] -= dt/1600
    spawn_rate[1] -= dt/1600
    new_bullets = []
    for bullet in bullets:
        if bullet.time > 0 and not bullet.destroy:
            new_bullets.append(bullet)
        else:
            bullet = None
    bullets = new_bullets
    new_boulders = []
    for bder in boulders:
        if (bder.hp <= 0):
            bder = None
            score += 100
        else :
            new_boulders.append(bder)
    boulders = new_boulders
    core.update(dt,boulders)

    if core.hp <= 0:
        #gameover
        pass
    if(shooting):
        if player.can_shoot():
            bullets.append(player.shoot(scroll,display))
    if move > 0:
        player.translate([player.speed*dt*1.5,0])
    elif move < 0:
        player.translate([-player.speed*dt,0])
    player.update(dt)
    for blt in bullets:
        blt.update(dt,boulders,tiles)
    for bder in boulders:
        bder.set_tiles(tiles)
        bder.update(dt)

    #---------------------------------------rendering---------------------------------------
    bg.render(display,scroll)
    #render_map(game_map_bg,display,bg_tileset,scroll,[],16)
    core.render(display,scroll)
    tiles = render_map(game_map,display,tileset,scroll,['1','2'])
    for bder in boulders:
        bder.render(display,scroll)
    for bullet in bullets:
        bullet.render(display,scroll)
    player.set_tiles(tiles)
    player.render(display,scroll)
    text = font.render("Score :" + str(score),True,(255,255,255))
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    screen.blit(text,(screen.get_width()/2 - 30,0))
    pygame.display.update()
    clock.tick(60)