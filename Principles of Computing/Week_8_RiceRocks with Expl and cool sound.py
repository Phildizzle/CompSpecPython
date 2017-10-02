# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
background_time = 0
animated_time = 0
best_score = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] += self.vel[1]
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle += self.angle_vel
        orient = angle_to_vector(self.angle)
        if self.thrust == True:
            self.vel[0] = (1- 0.012) * self.vel[0] + 0.23 * orient[0]
            self.vel[1] = (1- 0.012) * self.vel[1] + 0.23 * orient[1]
        elif self.thrust == False:
            self.vel[0] = (1- 0.012) * self.vel[0]
            self.vel[1] = (1- 0.012) * self.vel[1]
            
    def shoot(self):
        global a_missile
        orient = angle_to_vector(self.angle)
        a_missile = Sprite([self.pos[0] + 45 * orient[0],self.pos[1] + 45 * orient[1]] , [self.vel[0] + 10 * orient[0], self.vel[1] + 10 * orient[1]], 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) <= (self.radius + other_object.radius):
            return True
        else:
            return False
   
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        elif self.animated:
            global animated_time
            DIM = self.lifespan
            animated_index = (animated_time % DIM) // 1
            animated_center = [self.image_center[0] +  animated_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, animated_center, self.image_size, self.pos, self.image_size, self.angle) 
            animated_time += 1
           
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] += self.vel[1]
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age >= self.lifespan:
            return True
        elif self.age < self.lifespan:
            return False

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])      
        
# Update and draw the sprite group        
def process_sprite_group(group, canvas):
    for n in set(group):
        if n.update():
            group.remove(n)
        n.draw(canvas)
        
# Check if collide happens between a group and an object       
def group_collide(group, other_object):
    global explosion_group
    if_collide = False
    for n in set(group):
        if n.collide(other_object):
            group.remove(n)
            if_collide = True
            an_explosion = Sprite(n.pos, [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)        
    return if_collide

# Check if collide happens between two groups       
def group_group_collide(group1, group2):
    if_collide = False
    for n in set(group1):
        if group_collide(group2, n):
            group1.remove(n)
            if_collide = True
    return if_collide
        

def keydown(key):
    ship_angle_vel_inc = 0.15
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel -= ship_angle_vel_inc
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel += ship_angle_vel_inc
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrust = True
        my_ship.image_center = [135, 45]
        ship_thrust_sound.play()
    elif started and simplegui.KEY_MAP["space"] == key:
        my_ship.shoot()

def keyup(key):
    ship_angle_vel_inc = 0.15
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel += ship_angle_vel_inc
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel -= ship_angle_vel_inc     
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrust = False
        my_ship.image_center = [45, 45]
        ship_thrust_sound.rewind()

def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
        soundtrack.set_volume(0.3)
        
def draw(canvas):
    global background_time, lives, started, score, rock_group, best_score, my_ship
    
    # animiate background
    background_time += 1
    wtime = (background_time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship
    my_ship.update()
    
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    if lives == 0:
        started = False
        rock_group = set([])
        score = 0
        lives = 3
        soundtrack.rewind()
    
    if group_group_collide(missile_group, rock_group):
        score += 1
        if score > best_score:
            best_score = score
    
    canvas.draw_text("Lives : " + str(lives), (80, 80), 30, "White")
    canvas.draw_text("Score : " + str(score), (580, 80), 30, "White")
    canvas.draw_text("Best Score : " + str(best_score), (295, 80), 30, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship
    if started and len(rock_group) < 12:
        a_rock = Sprite([random.randrange(0,WIDTH), random.randrange(0,HEIGHT)], [-2 + random.random()*4, -2 + random.random()*4], 0, ( -0.1 + random.random()*0.2) , random.choice([asteroid_image1, asteroid_image2, asteroid_image3]), asteroid_info)
        if dist(a_rock.pos, my_ship.pos) >= (a_rock.radius + my_ship.radius + 30):
            rock_group.add(a_rock)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1100.0, rock_spawner)

# get things rolling
timer.start()
frame.start()