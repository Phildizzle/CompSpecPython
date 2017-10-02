"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    res = 0
    for dummy_dice in hand:
        temp = hand.count(dummy_dice) * dummy_dice
        if temp > res:
            res = temp 
    return res
    
def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    all_poss = gen_all_sequences([dummy_dice for dummy_dice in range(1,num_die_sides+1)], num_free_dice)
    return sum([score(held_dice + dummy_roll) for dummy_roll in all_poss]) / float(len(all_poss))
    
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    res = set([()])
    if len(hand) == 0:
        return res
    else:
        die_roll = hand[:-1]
        for dummy_tuple in gen_all_holds(die_roll):
            res.add(dummy_tuple)
            res.add((dummy_tuple + (hand[-1],)))

        return res



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    res = 0.0
    res_keep = ()
    for dummy_keep in gen_all_holds(hand):
        temp = expected_value(dummy_keep, num_die_sides, len(hand) - len(dummy_keep))
        if temp > res:
            res = temp
            res_keep = dummy_keep
            
    return (res, res_keep)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



