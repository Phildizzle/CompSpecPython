# Mini-project #6 - Blackjack
# by Philipp Knöpfle
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
# unfortunately I found no other card sprite, if you did, please send it via message to me :)
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_hand = []
dealer_hand = []
deck = []
outcome = ""
message = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
            
    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, x, y, card_cown):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [x + CARD_CENTER[0], y + CARD_CENTER[1]], CARD_SIZE)
        
        if card_cown:
            # first dealer_hand card position 
            card_loc = (CARD_CENTER[0], CARD_CENTER[1])
            # backside equivalent to the above function
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [x + CARD_CENTER[0], y + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return "Hand contains " + ' '.join([card.get_suit() + card.get_rank() for card in self.hand]) 
        ''' I love list comprehensions in Python so much, you can solve this with a for loop as well but the solution above
        is so much more elegant. '''
    
    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        hand_value = 0
        ace = False
        for card in self.hand:
            hand_value += VALUES.get(card.get_rank())
            if card.get_rank() == "A":
                ace = True
        if ace and hand_value < 11:
            return hand_value + 10
        else:
            return hand_value

    def hit(self, deck):
        self.add_card(deck.deal_card())
        
    def busted(self):
        ''' returns busted() = True when the hand value is over 21. This function
        allows me to cut back on a lot of conditional statements in the deal/hit/stand functions. 
        Thanks to the forums for the tip.'''
        global busted
        hand_value = self.get_value()
        if hand_value > 21:
            return True    
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand:
            card.draw(canvas, 50 + 80 * self.hand.index(card), pos, False)

# define deck class 
class Deck:
    def __init__(self):
        self.deck = [] # create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

#    def __str__(self):
#        return "Deck contains: " + ' '.join([card.get_suit() + card.get_rank() for card in self.deck]) 
# This is not really used in the game but since it was specified in the instructions here it is.

#define event handlers for buttons



def deal():
    global in_play, deck, dealer_hand, player_hand, score, outcome, message
    if in_play:
        score -= 1
        message = "Re-deal means score -= 1!"
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand() 
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
#    print "Player : " + str(player_hand) # remove after debug
#    print "Dealer : " + str(dealer_hand) # remove after debug
    in_play = True
    outcome = "Hit or stand?"
    
def hit():
    global in_play, score, outcome, message
    if in_play:
        player_hand.hit(deck)
        message = ""
        print str(player_hand)
        if player_hand.busted():
            outcome = "You got busted, mate!"
            in_play = False
            score -= 1
            message = "New deal?"
        elif player_hand.get_value() == 21:
            in_play = False
            outcome = "You got blackjack! You win."
            score += 1
            message = "New deal?"
               
def stand():
    global in_play, score, outcome, current
    message = ""
    if in_play:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

        while dealer_hand.get_value() < 17:
            dealer_hand.hit(deck)
            print str(dealer_hand)
        if dealer_hand.busted():
            outcome = "Dealer got busted!"
            score += 1
        elif player_hand.get_value() > dealer_hand.get_value():
            outcome = "You win, congratulations!"
            score += 1
        elif player_hand.get_value() == dealer_hand.get_value():
            outcome = "It's a tie, (unfortunately) the dealer wins!"
            score -= 1
        else:
            outcome = "Your hand is weaker!"
            score -= 1
    in_play = False
    message = "New deal?"
    
def reset():
    #set globals and initialize variables
    global score
    deal()
    score = 0    
    
# draw handler    
def draw(canvas):
    global in_play
    dealer_hand.draw(canvas, 200)
    player_hand.draw(canvas, 400)
    canvas.draw_text("Blackjack", (220,110), 38, "#DAA520")
    canvas.draw_text("Score: " + str(score), (250, 150), 26, "#000000")
    canvas.draw_text(outcome, (350, 180), 22, "#000000")
    canvas.draw_text(message, (350, 380), 22, "#000000")
    canvas.draw_text("Dealer", (170, 180), 26, "#000000")
    canvas.draw_text("Player", (170, 380), 26, "#000000")
    card = Card("S", "A")
    if in_play:
        card.draw(canvas, 50, 200, True) # True specifies "card_cown"

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 650)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Reset Score", reset, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

# remember to review the gradic rubric