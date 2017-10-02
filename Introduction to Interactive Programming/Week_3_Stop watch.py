# template for "Stopwatch: The Game"
import simplegui
# define global variables

count = 0
guesses = 0
right_guesses = 0
running = False
stop_state = True

HEIGHT = 300
WIDTH = 300
INTERVAL = 100

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """ Returns the string in a format A:BC:D, where max of A, C, D = 9
    and B = 5."""
    A = (t/10) // 60
    B = ((t/10) % 60) // 10
    C = ((t/10) % 60) % 10
    global D
    D = t % 10
    return str(A) + ":" + str(B) + str(C) + "." + str(D)    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running, stop_state
    running = True
    stop_state = False
    timer.start()
    
def stop():
    timer.stop()
    global guesses, right_guesses
    global D
    global running, stop_state
    running = False
    if not stop_state:
        guesses += 1
        if D == 0:
            right_guesses += 1
    stop_state = True
    
    
def reset():
    timer.stop()
    global count 
    count = 0
    global guesses, right_guesses
    guesses = 0
    right_guesses = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(str(format(count)), ((WIDTH/2-50), HEIGHT/2), 40, 'White')
    canvas.draw_text(str(right_guesses) + "/" + str(guesses), (240, 50), 30, 'Red')
    
# create frame and timer
frame = simplegui.create_frame("Stopwatch", HEIGHT, WIDTH)
timer = simplegui.create_timer(INTERVAL, tick)
frame.set_draw_handler(draw)
# register event handlers
frame.add_button('Start', start)
frame.add_button('Stop', stop)
frame.add_button('Reset', reset)

# start frame
frame.start()

# Please remember to review the grading rubric
