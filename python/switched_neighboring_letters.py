"""This script searches for word pairs which have the following properties:
1: length = 5,
2: the 2nd and 3rd characters or the 3rd and 4th characters are switched.
"""
import csv
import os.path
from os import listdir
from argparse import ArgumentParser
from common_funcs import read_words_from_file, create_mutants


# reading in args:
parser = ArgumentParser()

parser.add_argument('--length', type=str, default='5', metavar='N',
                        help='length of word pairs to find (default: 5)')

args = parser.parse_args()

length = int(args.length)

words_dir = os.path.join('..', 'words', str(args.length))
output_dir = os.path.join('output', 'switched_neighboring_letters')
output_file = args.length + '.csv'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# list to store the word pairs in:
word_pairs = []
all_words_checked = 0

# iterating over all files and find the ones which fulfill the criteria:
for file_name in listdir(words_dir):
    # reading the words from the actual file:
    word_list = read_words_from_file(words_dir, file_name)
    all_words_checked += len(word_list)

    if word_list != []:
        # creating some variables:
        words_done = []
        first_letter = word_list[0][0]

        for word in word_list:
            # creating list of posible mutants to search for:
            mutants = create_mutants(word=word, length=length)

            # searching for the mutants which are real words:
            for mutant in mutants:
                if mutant not in words_done:
                    if mutant[0] == first_letter:
                        if mutant in word_list:
                            # adding the found pair to the list:
                            word_pairs.append([word, mutant])
                            #print('found_pair: {}'.format([word, mutant]))
                    else:
                        # if the first letter does not match, the mutant has to be searched in an other file:
                        file_name2 = mutant[0] + '.csv'
                        word_list2 = read_words_from_file(words_dir, file_name2)

                        if mutant in word_list2:
                            # adding the found pair to the list:
                            word_pairs.append([word, mutant])
                            #print('found_pair: {}'.format([word, mutant]))

            # adding the word to the words done list
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