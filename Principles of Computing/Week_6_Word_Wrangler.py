"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math
import codeskulptor
codeskulptor.set_timeout(180)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    no_dupes = []
    [no_dupes.append(dummy_i) for dummy_i in list1 if not no_dupes.count(dummy_i)]
    return no_dupes

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    only_dupes = []
    [only_dupes.append(dummy_i) for dummy_i in remove_duplicates(list1) if dummy_i in remove_duplicates(list2)]
    return only_dupes

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    result = []
    lst1 = list(list1)
    lst2 = list(list2)
    
    while lst1 and lst2:
        if lst1[0] > lst2[0]:
            result.append(lst2.pop(0))
        else:
            result.append(lst1.pop(0))
    return result + lst1 + lst2
    
    
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    mid = math.floor(len(list1)/2)

    return merge(merge_sort(list1[:int(mid)]), merge_sort(list1[int(mid):]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    result = []
    
    if len(word) < 1:
           return [word]
    first = word[0]
    rest = word[1:]
    rest_strings = []
    rest_strings = gen_all_strings(rest)
    for dummy_i in rest_strings:
        if dummy_i == "":
            result.append(first)
        else:
            for dummy_j in range(len(dummy_i) + 1):
                front = dummy_i[:dummy_j]
                back = dummy_i[dummy_j:]
                new_string = front + first + back
                result.append(new_string) 
    return result + rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    
    data = []
    for line in netfile.readlines():
        word = line.strip()
        data.append(word)
    
    return data

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    