# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

secret_number = 0
max_guess = 0
max_range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    secret_number = random.randrange(0, max_range)
    global max_guess
    # calculate the logarithm with base two of the max range  
    # math.ceil basically rounds it up and delivers a float  
    # which we have to convert back into an int.
    max_guess = int(math.ceil(math.log(max_range + 1, 2)))
    print "Number of remaining guesses: " + str(max_guess)

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global max_range
    max_range = 100
    new_game()
    print "\nNew game with range 1-99 has started."

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global max_range
    max_range = 1000
    new_game()
    print "\nNew game with range 1-999 has started."
    
def input_guess(guess):
    # main game logic goes here	
    print "Guess was: " + guess
    guess =  int(guess)
    
    global max_guess
    max_guess -= 1
    print "Number of remaining guesses: " + str(max_guess)
    if guess == secret_number:
        print "Correct!\n"
        print "Let's start a new game!"
        new_game()
    elif guess < 0:
        print "Negative numbers are not supported :)!"
    else:
        if max_guess == 0:
            print "Sorry you ran out of guesses!\n"
            print "Let's start a new game!"
            new_game()
        else:
            if guess < secret_number:
                print "Higher!\n"
            else:
                print "Lower!\n"

# create frame
frame = simplegui.create_frame("Guess the number", 400, 400)

# register event handlers for control elements and start frame
frame.add_input("Enter guess for number", input_guess, 75)
frame.add_button("Range is [0,100)", range100, 100)
frame.add_button("Range is [0,1000)", range1000, 100)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
