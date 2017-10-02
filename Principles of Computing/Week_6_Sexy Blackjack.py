# Mini-project #6 - Blackjack

import simplegui
import random as rand

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
prompt = ""
player_score = 0
dealer_score = 0


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

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        output = "Hand contains "
        for card in self.cards:
            output += str(card) + " "
        return output    
            # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        aced = False
        for card in self.cards:
            rank = card[1]
            value += VALUES[rank]
            if rank == 'A':
                aced = True
        if aced and 10+value <= 21:
            value + 10
        return value 
   
    def draw(self, canvas, pos):
        i = 0
        loc = [0,pos[1]]
        for card in self.cards:
            loc[0] = pos[0] + i * 78 
            Card(card[0], card[1]).draw(canvas, loc)
            i += 1

        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(suit+rank)# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        rand.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop()	# deal a card object from the deck
    
    def __str__(self):
        output = "Deck contains "
        for card in self.deck:
            output += str(card) + " "
        return output 
            # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer, player, prompt
    # initialize the deck
    deck = Deck()
    # shuffle the deck
    deck.shuffle()
    # initialize empty hands
    dealer = Hand()
    player = Hand()
    # deal to both hands
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    outcome = "Cards dealt!"
    prompt = "Hit or stand?"
    # Print to console
    print("")
    print("New deal start!")
    print("")
    print("For the dealer:")
    print(str(dealer))
    print("For the player:")
    print(str(player))
    
    print(str(player_score))
    in_play = True

def hit():
    global in_play, outcome, prompt, player_score, dealer_score
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score 
        # Print to console
        print("")
        print("You hit.")
        outcome = "You hit."
        print("")
        print("For the dealer:")
        print(str(dealer))
        print("For the player:")
        print(str(player))

        if player.get_value() > 21:
            print("")
            print("You have busted!")
            outcome = "You hit. You have busted!"
            print("The dealer wins!")
            dealer_score += 1
            prompt = "The dealer wins! New deal?"
            in_play = False
            
        
def stand():
    global in_play, outcome, prompt, player_score, dealer_score
    if in_play:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        #if player.get_value() > 21:
              #  print("You have busted!")
                #print("The dealer wins!")
                #print("")
                #in_play = False
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        
        # Print to console
        print("")
        print("You stand.")
        print("")
        print("For the dealer:")
        print(str(dealer))
        print("For the player:")
        print(str(player))
    
        if dealer.get_value() > 21:
            print("")
            print("The dealer has busted!")
            outcome = "You stand. The dealer has busted!"
            print("You win!")
            player_score += 1
            prompt = "You win! New deal?"
            print("")
            in_play = False
        elif player.get_value() <= dealer.get_value():
            print("")
            outcome = "You stand."
            print("The dealer wins!")
            dealer_score += 1
            prompt = "The dealer wins! New deal?"
            print("")
            in_play = False
        else:
            print("")
            outcome = "You stand."
            print("You win!")
            prompt = "You win! New deal?"
            player_score += 1
            print("")
            in_play = False
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_image(image, (408, 204), (408, 408), (300, 300), (600, 600))
    #canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest)     
    # Print hands
    dealer.draw(canvas, [50,150])
    player.draw(canvas, [50,450])
    # Cover dealer hole
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [86,198], CARD_SIZE)
    
    # Text msgs
    canvas.draw_text("Blackjack", (10,50), 65, 'white', 'monospace')
    canvas.draw_text("Dealer's Hand:", (10,140), 25, 'white', 'serif')
    canvas.draw_text("Your Hand:", (10,440), 25, 'white', 'serif')
    # Prompt and status messages
    canvas.draw_text(outcome, (10,325), 33, 'white', 'serif')
    status_pos = (10,360)
    if in_play:
        canvas.draw_text(prompt, status_pos, 33, 'white', 'serif')
    else:
        canvas.draw_text(prompt, status_pos, 33, 'white', 'serif')
    # score box
    canvas.draw_line((9,80),(361,80), 22, 'white')
    canvas.draw_line((10,80),(360,80), 20, 'black')
    canvas.draw_circle((180,80), 12, 2, "white", "#049D2A")
    #canvas.draw_line(point1, point2, line_width, line_color)
    canvas.draw_text("Player                 "+str(player_score), (11,87), 20, 'white', 'serif')
    canvas.draw_text("Dealer                 "+str(dealer_score), (200,87), 20, 'white', 'serif')
    
    #canvas.draw_text(text, point, font_size, font_color, font_face)             

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
image = simplegui.load_image('http://media.istockphoto.com/photos/green-felt-and-playing-chips-abstract-background-picture-id672556284?k=6&m=672556284&s=612x612&w=0&h=ofClcfW6AHnx698r8tB-EIvdaajhch9I-Y2aH3bw4A4=')
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric