# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PAD_TOP_HEIGHT = HEIGHT - HALF_PAD_HEIGHT
HALF_HEIGHT = HEIGHT/2
HALF_WIDTH = WIDTH/2
init_pos = [WIDTH/2, HEIGHT/2]
time = 0
ball_pos = [0,0]
ball_vel = [0, 0]
PAD_VEL = 4


# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_vel = [random.randrange(2,4), - random.randrange(1,3)]
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == LEFT:
        ball_vel[0] = - ball_vel[0]

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2 # these are ints
    
    paddle1_pos = HALF_HEIGHT
    paddle2_pos = HALF_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(random.choice([RIGHT, LEFT]))
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos > PAD_TOP_HEIGHT:
        paddle1_pos = PAD_TOP_HEIGHT
    elif paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel

    if paddle2_pos > PAD_TOP_HEIGHT:
        paddle2_pos = PAD_TOP_HEIGHT
    elif paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    else:
        paddle2_pos += paddle2_vel        
    
    # draw mid line and gutters
    canvas.draw_line([HALF_WIDTH, 0],[HALF_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    
    # draw paddles
    paddle1_top_pos = paddle1_pos + HALF_PAD_HEIGHT
    paddle1_bot_pos = paddle1_pos - HALF_PAD_HEIGHT
    paddle2_top_pos = paddle2_pos + HALF_PAD_HEIGHT
    paddle2_bot_pos = paddle2_pos - HALF_PAD_HEIGHT

    canvas.draw_line([HALF_PAD_WIDTH, paddle1_top_pos], [HALF_PAD_WIDTH, paddle1_bot_pos], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_top_pos], [WIDTH - HALF_PAD_WIDTH, paddle2_bot_pos], PAD_WIDTH, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # collision top or bottom
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    

    # determine whether paddle and ball collide
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if paddle1_top_pos >= ball_pos[1] >= paddle1_bot_pos:
            ball_vel[0] = -ball_vel[0]*1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if paddle2_top_pos >= ball_pos[1] >= paddle2_bot_pos:
            ball_vel[0] = -ball_vel[0] 
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)                     

    # draw scores
    canvas.draw_text(str(score1), [120,60], 30, "White")
    canvas.draw_text(str(score2), [480,60], 30, "White")

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 4, "White", "White")            
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= PAD_VEL
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += PAD_VEL
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= PAD_VEL
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += PAD_VEL
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New game", new_game, 50)


# start frame
new_game()
frame.start()
