import time,pygame

def calc_dt(old_time):
    current_time = time.time()
    dt = current_time - old_time
    dt *= 60
    return dt,current_time

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    game_map = []
    f.close()
    data = data.split('\n')
    for row in data:
        game_map.append(list(row))
    return game_map

def render_map(map,display,tileset,scroll,collidabe_tiles,tile_size = 16):
    tile_rects = []
    y = 0
    for row in map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(tileset[0],(x*tile_size - scroll[0],y*tile_size - scroll[1]))
            if tile == '2':
                display.blit(tileset[1],(x*tile_size - scroll[0],y*tile_size - scroll[1]))
            if tile in collidabe_tiles:
                tile_rects.append(pygame.Rect(x*tile_size,y*tile_size,tile_size,tile_size))
            x += 1
        y += 1
    return tile_rects

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

def load_animation(path,frame_duration,animation_frames):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        image_loc = path + '/' + str(n) + '.png'
        animation_image = pygame.image.load(image_loc)
        animation_frames[animation_name + str(n)] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_name + str(n))
        n+=1
    return animation_frame_data