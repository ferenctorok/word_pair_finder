"""This script searches for word pairs where the second word is gotten from the first by augmenting it 
by a letter anywhere but at the end or at the beginning.
"""
import csv
import os.path
import numpy as np
from os import listdir
from argparse import ArgumentParser
from common_funcs import read_words_from_file, get_shortened_list_by_index


# reading in args:
parser = ArgumentParser()

parser.add_argument('--length', type=str, default='5', metavar='N',
                        help='length of word pairs to find (default: 5)')

args = parser.parse_args()

length = int(args.length)

words_dir_short = 'words/' + args.length
words_dir_long = 'words/' + str(length + 1)
output_dir = 'output/extra_letter_in_between'
output_file = args.length + '.csv'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# list to store the word pairs in:
word_pairs = []
all_words_checked = 0

# iterating over all files and find the ones which fulfill the criteria:
for file_name in listdir(words_dir_short):
    # reading the words from the actual file:
    word_list_short = read_words_from_file(words_dir_short, file_name)
    all_words_checked += len(word_list_short)

    # reading the words from the file that contains the one letter longer words:
    word_list_long = read_words_from_file(words_dir_long, file_name)
    
    if word_list_long != []:
        for index in range(1, length-1, 1):
            # creating a shortened version from it:
            word_list_long_shortened = get_shortened_list_by_index(word_list_long, index)

            # converting the long lists into numpy array for easier search:
            word_list_long = np.array(word_list_long)
            word_list_long_shortened = np.array(word_list_long_shortened)

            for word in word_list_short:
                if word in word_list_long_shortened:
                    indices = np.where(word_list_long_shortened == word)
                    word_pair_list = list(word_list_long[indices])

                    # storing the found pairs in word_pairs:
                    for pair in word_pair_list:
                        word_pairs.append([word, pair])

    print('{} is done.'.format(os.path.join(words_dir_short, file_name)))

print('finding pairs is done.')
if word_pairs != []:
    print('Checked {} words, found {} pairs.'.format(all_words_checked, len(word_pairs)))
else:
    print('Checked {} words, didn\'t find any pairs.'.format(all_words_checked))

# writing output file:
output_path = os.path.join(output_dir, output_file)
print('writing pairs into: {}'.format(output_path))

with open(output_path, 'w') as f:
    writer = csv.writer(f, delimiter=',')
    for pair in word_pairs:
        writer.writerow(pair)

print('writing output in file {} is done.'.format(output_path))