import csv
import os.path
import queue


def read_words_from_file(words_dir, file_name):
    file_path = os.path.join(words_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf8") as f:
            reader = csv.reader(f, delimiter=',')
            word_list = list(reader)[0][:]
    else:
        word_list = []
    
    return word_list


def get_shortened_list(long_list):
    shortened_list = []
    for item in long_list:
        shortened_list.append(item[0:-1])

    return shortened_list


def get_shortened_list_by_index(long_list, index):
    shortened_list = []
    for item in long_list:
        shortened_item = item[0: index] + item[index + 1:]
        shortened_list.append(shortened_item)

    return shortened_list


def create_mutants(word, length):
    mutants = []

    for i in range(length - 1):
        # creating a mutant with switched letters:
        mutant = list(word)
        mutant[i] = word[i + 1]
        mutant[i + 1] = word[i]
        mutant = ''.join(mutant)

        # if the mutant is different from the original word it is added to the list:
        if mutant != word:
            mutants.append(mutant)
    
    return mutants

class SearchTreeNode:
    """A node for easier search through words with search tree techniques.
    
    fields:
        - word: word in the node
        - parent: parent node if there is any. None if it has no parent.
        - search_horizon: length of words to look for as possible successor words.
        - has_been_saved: whether the node has been already saved as a node of a branch
    """
    def __init__(self, word=None, parent=None):
        self.word = word
        self.sarch_horizon = len(word)
        self.parent = parent
        self.has_been_saved = False
    
    def set_value(self, value):
        self.value = value
    
    def set_parent(self, parent):
        self.parent = parent
    
    def Expand_search_horizon(self):
        """Increases the horizon to search for with 1."""
        self.sarch_horizon += 1

    def set_parents_as_saved(self):
        """Setting all the parent node's has_been_saved field to saved."""
        parent = self.parent

        while parent is not None:
            parent.has_been_saved = True
            parent = parent.parent

    def __repr__(self):
        print('SearchTreeNode:')
        print('word: {}'.format(self.word))
        print('parent: {}'.format(self.parent))
        print('sarch_horizon: {}'.format(self.sarch_horizon))
        print('has_been_saved: {}'.format(self.has_been_saved))