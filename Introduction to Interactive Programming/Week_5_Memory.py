# implementation of card game - Memory

import simplegui
import random

first_card = 0
second_card = 0


state = 0
# helper function to initialize globals
def new_game():
    global state, turns, deck, exposed
    state = 0
    turns = 0
    deck = [i%8 for i in range(16)]
    exposed = [False] * 16
    random.shuffle(deck)
    label.set_text("Turns: " + str(turns))

# define event handlers
def mouseclick(pos):
    global state, exposed, first_card, second_card, turns, deck
    pick = (pos[0] // 50)
    if state == 0:
        first_card = pick
        exposed[first_card] = True
        state = 1
    elif state == 1:
        if not exposed[pick]:
            second_card = pick
            exposed[second_card] = True
            turns += 1
            label.set_text("Turns: " + str(turns))
            state = 2
    elif state == 2:
        if not exposed[pick]:
            if deck[first_card] == deck[second_card]:
                pass
            else:
                exposed[first_card] = False
                exposed[second_card] = False
            first_card = pick
            exposed[first_card] = True
            state = 1
pass
        
# cards are logically 50x100 pixels in size, 
# but I made them 50x110 so it looks nicer ;)   
def draw(canvas):
    global deck
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(deck[i]), [ 20 + i * 50, 62], 24, "White")
        else:
            canvas.draw_polygon([(50 * i, 0), ((i + 1) * 50, 0), ((i + 1) * 50, (i + 1) * 110), (i * 50, 110)], 5, "Fuchsia", "Purple")
    
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric