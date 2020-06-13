"""
Student code for Word Wrangler game
"""

# import urllib2
# import codeskulptor
from poc.word_wrangler import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    deduplicated_list = list()
    for item in list1:
        if item not in deduplicated_list:
            deduplicated_list.append(item)
    return deduplicated_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersect_list = []
    deduplicated_list1 = remove_duplicates(list1)
    for item in deduplicated_list1:
        if item in list2:
            intersect_list.append(item)
    return intersect_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    size_1 = len(list1) 
    size_2 = len(list2) 
    
    res = [] 
    i, j = 0, 0
    
    while i < size_1 and j < size_2: 
        if list1[i] < list2[j]: 
            res.append(list1[i]) 
            i += 1
        else: 
            res.append(list2[j]) 
            j += 1
    
    res = res + list1[i:] + list2[j:] 
    return res
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    else:
        pivot = list1[0]
        pivot_list = [item for item in list1 if item == pivot]
        other_list = [item for item in list1 if item != pivot]
        return merge(merge_sort(other_list), pivot_list)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    assert type(word) == str
    if word == "":
        return [word]
    else:
        first = word[0]
        rest = word[1:]
        first_strings = []
        rest_strings = gen_all_strings(rest)
        print("first:", first)
        for item in rest_strings:
            print("item:", item)
            for idx in range(len(item) + 1):
                new_word = item[:idx] + first + item[idx:]
                print("new word:", new_word)
                first_strings.append(new_word)
        print(rest_strings + first_strings)
        return rest_strings + first_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

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
# run()  