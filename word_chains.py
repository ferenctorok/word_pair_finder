"""This script searches for word sequences. Each sequence consists of at least 'min_words' number of words.
Every sequence starts from a basis word and the other words are built from it by adding extra parts to it. 

We would like to avoid sub chains (shown below). For this depth first search like algorithm is used:
chain: abc - abcd - abcde - abcdef
sub chain: abc - abcde - abcdef

ALGORITHM:
explored_words = []
word_chains = []

For every word if word is not in explored_words:
    init LIFO queue word (node.word = word, node.parent = None)
    leaf_nodes = []
    while LIFO queue is not empty:
        Pop a node from the LIFO queue.
        node.expand_search_horizon()   # increases the length of words to be searched for by 1.
        new_successors = search_for_successors(node.exploration_length)
        set all new_successor's parent = node
        If node.search_horizon == max_word_length
            If (new_successors == []) and not node.has_been_saved:
                leaf_nodes += node
                node.set_parents_as_saved()
            Else:
                leaf_nodes += new_successors
                For successor in new_successors:
                    succesor.set_parents_as_saved()
                End For
            End If
        Else:
            push node back into LIFO queue
            push successors into LIFO queue
        End If            
    End While

    For leaf in leaf_nodes:
        word_chain = get_branch_of_leaf(leaf)
        word_chains.append(word_chain)
        explored_words += word_chain
    End For
End For
"""

import csv
import os.path
import numpy as np
from os import listdir
from argparse import ArgumentParser
from common_funcs import read_words_from_file, get_shortened_list


# reading in args:
parser = ArgumentParser()

parser.add_argument('--first-min-length', type=int, default='2', metavar='N',
                    help='Minimum length of the first word in the chain (default: 2)')

parser.add_argument('--first-max-length', type=int, default='8', metavar='N',
                    help='Maximum length of the first word in the chain (default: 2)')

parser.add_argument('--min-chain-length', type=int, default='3', metavar='N',
                    help='Min length of word chain (default: 2)')

args = parser.parse_args()

# the length of the first word can range from first_min_length to first_max_length
first_min_length = args.first_min_length
first_max_length = args.first_max_length
possible_first_word_lengths = list(range(first_min_length, first_max_length + 1, 1))

# current downloaded longest word set:
max_word_length = 10

# minimum length of word chains to finds
min_chain_length = args.min_chain_length

output_dir = 'output/word_builder'
output_file = args.length + '.csv'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# already used words:
used_words = []

for first_word_length in possible_first_word_lengths:
    # breaking the loop if we can not build sufficiently long chains starting with a this long word:
    if (first_word_length + min_chain_length - 1) > max_word_length:
        break
    
    # actual search dir for the first word in the chain:
    first_words_dir = 'words/' + str(first_word_length)

    # the possible lengths of the following words in the chain:
    possible_following_word_lengths = list(range(first_word_length + 1, max_word_length, 1))

    for following_word in following_words_dir:
        following_words_dir = 'words/' + str(following_word)

    










