import numpy as np
import urllib.request
from urllib.parse   import quote
from bs4 import BeautifulSoup
import os.path
from os import remove
import csv
from argparse import ArgumentParser

# some global variables:
WIKI_URL = 'https://hu.wiktionary.org/wiki/Index:Magyar'
ABC = ['a', 'b', 'c', 'cs', 'd', 'dz', 'dzs', 'e', 'é', 'f', 'g', 'gy', 'h', 'i', 'j', 'k', 'l', 'ly', 'm', 'o', 'ö', 'ő',
        'p', 'q', 'r', 's', 'sz', 't', 'ty', 'u', 'ú', 'ü', 'v', 'w', 'x', 'y', 'z', 'zs']
LENGTHS = [2, 3]
DATA_DIR = 'words'


def get_words_from_link(url, html_dir='words/html', html_file='html.txt'):
    """This function downloads the html of a wiktionary page and extracts the words from it."""
    
    # creating the directory if it does not exist:
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    
    # reading the html of the site and storing it in the target file:
    urllib.request.urlretrieve(url, os.path.join(html_dir, html_file))
    
    # parsing the html:
    with open(os.path.join(html_dir, html_file)) as f:
        soup = BeautifulSoup(f.read())
    
    # deleting the text file
    os.remove(os.path.join(html_dir, html_file))
    
    # finding all the parts of the html which list the words:
    h2_tags = soup.find_all('p')
    a_tags = []
    for tag in h2_tags:
        a_tags += tag.find_all('a')

    h2_tags = None

    # extracting the text (words):
    word_list = []
    for line in a_tags:
        word_list.append(line.text)
        
    return word_list    


def write_words_to_files(word_list, data_dir='words', letter='a', lengths=[]):
    """This function saves the words in word list into csv files according to their lengths.
    It creates a directories under data_dir with the corresponding lengths and saves the words
    starting nto csv files under these directories.
    Inputs: 
        word_list: list of strings.
        data_dir: directory where folders for the different lengts are going to be created.
        letter: initial letter of the words in word list. (also the name of the csv files)
        lengths: specified lengths of words which need to be saved.
    """
    for length in lengths:
        # current directory to save words with length:
        current_dir = os.path.join(data_dir, str(length))
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
        
        # extracting the words with length:
        words_of_length = [word for word in word_list if len(word) == length]

        # writing the csv file:
        file_name = letter + '.csv'
        with open(os.path.join(current_dir, file_name), 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(words_of_length)    

    print('writing the words with \'{}\' and lengths {} is done.'.format(letter, lengths))


def download_words_from_wiki(wiki_link='https://hu.wiktionary.org/wiki/Index:Magyar',
                             letters=[], lengths=[], data_dir='words'):
    """This function downloads all the hunarian words from the wikipedia with the firs letters specified in letters,
    and the lengths specified in lengths. It saves the words under data_dir in a structure that the words with common lengths
    are stored in a dir with the name that corresponds to the length. under these dirs the words are stored in csv files according
    to their first letters.
    inputs: 
        wiki_link: uri under which the words can be found in wictionary.
        letters: list of lettters to be downloaded
        lengths: list of word lengths to be saved.
        data_dir: directory to save
    """

    for letter in letters:
        # creating the url for the letter:
        #actual_url = u'{}'.format((wiki_link + '/' + letter).encode('utf-8'))
        actual_url = wiki_link + '/' + quote(letter)
        # downloading the words starting with letter:
        html_dir = os.path.join(data_dir, 'html')
        word_list = get_words_from_link(url=actual_url, html_dir=html_dir, html_file='html.txt')

        # saving the words with specified lengths:
        write_words_to_files(word_list=word_list, data_dir=data_dir, letter=letter, lengths=lengths)

        # deleting word_list:
        word_list = None
    
    print('Downloading words from wikipedia is done. Results are saved in {} folder.'.format(data_dir))


if __name__ == '__main__':

    parser = ArgumentParser()

    # parameters:
    parser.add_argument('--wiki_link', type=str, default=WIKI_URL, metavar='N',
                        help='wikipedia url (default: {})'.format(WIKI_URL))

    parser.add_argument('--letters', nargs='+', type=int, default=ABC, metavar='N',
                        help='letters to download (default: {})'.format(ABC))

    parser.add_argument('--lengths', nargs='+', type=int, default=LENGTHS, metavar='N',
                        help='letters to download (default: {})'.format(LENGTHS))

    parser.add_argument('--data_dir', type=str, default=DATA_DIR, metavar='N',
                        help='directory to save in (default: {})'.format(DATA_DIR))

    
    args = parser.parse_args()

    download_words_from_wiki(wiki_link=args.wiki_link,
                             letters=args.letters,
                             lengths=args.lengths,
                             data_dir=args.data_dir)

    

