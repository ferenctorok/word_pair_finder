import csv
import os.path


def read_words_from_file(words_dir, file_name):
    file_path = os.path.join(words_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
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