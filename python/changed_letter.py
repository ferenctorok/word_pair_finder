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

words_dir = os.path.join('..', 'words', str(args.length))
output_dir = os.path.join('output', 'changed_letter')
output_file = args.length + '.csv'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# list to store the word pairs in:
word_pairs = []
words_done = []
all_words_checked = 0

# iterating over all files and find the ones which fulfill the criteria:
for file_name in listdir(words_dir):
    # reading the words from the actual file:
    word_list = read_words_from_file(words_dir, file_name)
    all_words_checked += len(word_list)

    if word_list != []:
        # converting the word list into np array for easier searching:
        word_list = np.array(word_list)

        for index in range(length):
            words_done = []

            if index == 0:
                # if the first letter is changed all the files has to be checked:
                for file_name2 in listdir(words_dir):
                    # reading the words from the actual file:
                    word_list2 = read_words_from_file(words_dir, file_name2)

                    # creating the shortened list:
                    word_list_shortened = get_shortened_list_by_index(word_list2, index)

                    # converting the lists into numpy array for easier search:
                    word_list2 = np.array(word_list2)
                    word_list_shortened = np.array(word_list_shortened)

                    for word in word_list:
                        # cutting out the letter at index from word:
                        word_shortened = word[index + 1:]

                        indices = np.where(word_list_shortened == word_shortened)
                        word_pair_list = list(word_list2[indices])

                        # storing the found pairs in word_pairs:
                        for pair in word_pair_list:
                            if pair != word:
                                word_pairs.append([word, pair])

            else:
                # creating the shortened list:
                word_list_shortened = get_shortened_list_by_index(word_list, index)

                # converting the shortened list into numpy array for easier search:
                word_list_shortened = np.array(word_list_shortened)

                for word in word_list:
                    # cutting out the letter at index from word:
                    word_shortened = word[0: index] + word[index + 1:]

                    indices = np.where(word_list_shortened == word_shortened)
                    word_pair_list = list(word_list[indices])

                    # storing the found pairs in word_pairs:
                    for pair in word_pair_list:
                        if pair != word and pair not in words_done:
                            word_pairs.append([word, pair])

                    words_done.append(word)

    print('{} is done.'.format(os.path.join(words_dir, file_name)))

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