import pygame,sys,DarkEngine,time,math,random,core #modules
import player,backgroud,boulder #game files
from pygame.locals import *
from DarkEngine import *

#---------------------------------------constants---------------------------------------
WINDOW_SIZE = (1920,1080)
#WINDOW_SIZE = (1280,720)
#WINDOW_SIZE = (960,540)
#WINDOW_SIZE = (640,360)
DISPLAY_SIZE = (1280,720)

#--------------------------------------PYGAME SETUP---------------------------------------
pygame.init()
pygame.mixer.init(44000,-16,2,1024)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface(DISPLAY_SIZE)

#--------------------------------------SOUNDS---------------------------------------------
sounds = {'shoot' : pygame.mixer.Sound('sounds/shoot.wav'),
          'gameover' : pygame.mixer.Sound('sounds/gameover.wav'),
          'buff' : pygame.mixer.Sound('sounds/buff.wav'),
          'explosion' : pygame.mixer.Sound('sounds/explosion.wav'),
          'destroy' : pygame.mixer.Sound('sounds/destroy.wav'),
          'jump' : pygame.mixer.Sound('sounds/jump.wav'),
          'hit' : pygame.mixer.Sound('sounds/hit.wav'),
          'select' : pygame.mixer.Sound('sounds/select.wav'),
          'click' : pygame.mixer.Sound('sounds/click.wav')}
music = pygame.mixer.music.load('music/loop.wav')

#--------------------------------------FILE LOADING---------------------------------------
game_map = load_map('map/map1')
game_map_bg = load_map('map/map1bg')
tileset = [pygame.image.load('images/surface.png').convert(),
           pygame.image.load('images/ground.png').convert()]
bg_tileset = [pygame.image.load('images/spaceshipbg.png').convert()]
boulders = []
bullets = []

title = pygame.transform.scale(pygame.image.load('images/title.png'),(1400,700))
play_button = pygame.image.load('images/play_button.png')
quit_button = pygame.image.load('images/quit_button.png')
help_button = pygame.image.load('images/help_button.png')
play_rect = pygame.Rect(WINDOW_SIZE[0] - 135,WINDOW_SIZE[1] - 880,123,45)
quit_rect = pygame.Rect(WINDOW_SIZE[0] - 135,WINDOW_SIZE[1] - 280,123,45)
help_rect = pygame.Rect(WINDOW_SIZE[0] - 135,WINDOW_SIZE[1] - 580,123,45)

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
font1 = pygame.font.Font('font/OZOBAROF PERSONAL USE.ttf',32)
font2 = pygame.font.Font(None,56)
font3 = pygame.font.Font(None,42)
spawn_rate = [5,7]
spawn_timer = 0
score = 0
GAME_STATES = {'Menu' : 1,'Game' : 2}
game_state = GAME_STATES['Menu']
play = False
quitt = False
tuto_text = ["W to jump,A and D to move",
          "left click to shoot and right click to swtch firing mode",
          "left click on left side to shoot left and vice versa",
          "protect the ship core from falling boulder",
          "full auto fire deals high damage up close",
          "semi auto fire deals low damage close but very high damage at range",
          "touching a boulder or letting 5 boulders hit the core will end the game"]
score_text = ""
gameover_text = ""
show_tutorial = False
particles = []
for x in range(80):
    particles.append([(random.randint(0,WINDOW_SIZE[0]),random.randint(0,WINDOW_SIZE[1])),random.randint(1,4),random.randint(10,40)/10])
rocks = []
rock_img = pygame.image.load('images/boulder_0.png')
for x in range(40):
    rocks.append([[random.randint(-1500,WINDOW_SIZE[0] - 500),random.randint(-1200,-100)],random.randint(20,30)/10,random.randint(32,64)])

#---------------------------------------MORE INIT---------------------------------------
tiles = render_map(game_map,display,tileset,[0,0],['1','2'])
player.set_tiles(tiles)
for bder in boulders:
    bder.set_tiles(tiles)

#---------------------------------------GAME LOOP---------------------------------------
while True:
    if game_state == GAME_STATES['Menu']:
        screen.fill((0,0,20))

        for particle in particles:
            particle[0] = (particle[0][0] + particle[2],particle[0][1])
            if(particle[0][0] >= WINDOW_SIZE[0] + particle[2]):
                particle[0] = (0,random.randint(0,WINDOW_SIZE[1]))
            pygame.draw.circle(screen,(255,255,255),particle[0],particle[1])
        for rock in rocks:
            rock[0] = (rock[0][0] + rock[1],rock[0][1] + rock[1])
            if(rock[0][1] >= WINDOW_SIZE[0] + rock[1]):
                rock[0] = [random.randint(-1500,WINDOW_SIZE[0] - 500),random.randint(-1200,-100)]
            screen.blit(pygame.transform.scale(rock_img,(rock[2],rock[2])),(rock[0][0],rock[0][1]))
        mx,my = pygame.mouse.get_pos()
        if play_rect.collidepoint(mx,my):
            if not play:
                sounds['select'].play()
            play = True
            pygame.draw.rect(screen,(255,255,255),play_rect,2)
        elif quit_rect.collidepoint(mx,my):
            if not quitt:
                sounds['select'].play()
            quitt = True
            pygame.draw.rect(screen,(255,255,255),quit_rect,2)
        elif help_rect.collidepoint(mx,my):
            if not show_tutorial:
                sounds['select'].play()
            show_tutorial = True
            pygame.draw.rect(screen,(255,255,255),help_rect,2)
        else:
            quitt = False
            show_tutorial = False
            play = False

        go_txt = font2.render(gameover_text,True,(255,160,160))
        sc_txt = font2.render(score_text,True,(255,255,255))
        screen.blit(go_txt,(WINDOW_SIZE[0]/2 - 100,WINDOW_SIZE[1]/2))
        screen.blit(sc_txt,(WINDOW_SIZE[0]/2 - 115,WINDOW_SIZE[1]/2 + 50))
        screen.blit(title,(WINDOW_SIZE[0]/2 - 700,WINDOW_SIZE[1]/2 - 400 - 175))
        screen.blit(play_button,(WINDOW_SIZE[0] - 500,WINDOW_SIZE[1]- 900))
        screen.blit(quit_button,(WINDOW_SIZE[0] - 500,WINDOW_SIZE[1] - 300))
        screen.blit(help_button,(WINDOW_SIZE[0] - 500,WINDOW_SIZE[1] - 600))
        if(show_tutorial):
            for index,txt in enumerate(tuto_text):
                tutorial =  font3.render(tuto_text[index],True,(255,255,255))
                screen.blit(tutorial,(0,700 + 40*index))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    sounds['click'].play()
                    if(play):
                        play = False
                        player.set_pos([1060,700])
                        scroll = [0,0]
                        core.hp = 50
                        boulders = []
                        player_action = 'idle'
                        player_frame = 0
                        old_time = time.time()
                        shooting = False
                        move = 0
                        player.died = False
                        spawn_rate = [10,15]
                        player.died = False
                        spawn_timer = 0
                        score = 0
                        pygame.mixer.music.play(-1)
                        game_state = GAME_STATES['Game']
                    if(quitt):
                        quitt = False
                        pygame.quit()
                        sys.exit()
        pygame.display.update()
        clock.tick(60)

    if game_state == GAME_STATES['Game']:
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

        if(move >= 0.5 or move <= -0.5):
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
        spawn_rate[0] -= dt/1000
        spawn_rate[1] -= dt/1000
        new_bullets = []
        for bullet in bullets:
            if bullet.time > 0 and not bullet.destroy:
                new_bullets.append(bullet)
            else:
                bullet = None
        bullets = new_bullets
        new_boulders = []
        for bder in boulders:
            if bder.hp <= -1000:
                pass
            elif (bder.hp <= 0):
                bder = None
                sounds['buff'].play()
                sounds['destroy'].play()
                score += 100
            else :
                new_boulders.append(bder)
        boulders = new_boulders
        core.update(dt,boulders,sounds['explosion'])
        if core.hp <= 0 or player.died:
            score_text = 'last score : ' + str(score)
            gameover_text = "Game Over"
            game_state = GAME_STATES['Menu']
            pygame.mixer.music.stop()
            print('done')
            continue
        if(shooting):
            if player.can_shoot():
                bullets.append(player.shoot(scroll,display,sounds['shoot']))
        if move > 0:
            player.translate([player.speed*dt*1.5,0])
        elif move < 0:
            player.translate([-player.speed*dt,0])
        player.update(dt,sounds['jump'],boulders)
        for blt in bullets:
            blt.update(dt,boulders,tiles,sounds['hit'])
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
        text = font1.render("Score :",True,(255,255,255))
        text2 = font2.render(str(score),True,(255,255,255))
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        screen.blit(text,(screen.get_width()/2 - 40,0))
        screen.blit(text2,(screen.get_width()/2 + 50,0))
        pygame.display.update()
        clock.tick(60)
