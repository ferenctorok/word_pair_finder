# Findig special Hungarian word pairs #

This project was created in order to help my mother to find special Hungarian word pairs. She works as a speech therapist and developmental teacher in a primary school.
In the last times she has been searching for special word pairs, such for example which differ from eachother in only one letter, for writing tasks for children.
This is a very time consuming and nerve wracking task and is very easily automatizable. Hence I have written this project to automatize the search for word pairs.

## Install ##
### Required packages ###
- numpy
- os
- argparse
- urllib3
- BeautifulSoup4
- jupyter

Install and activate the environment from the `environment.yml` file using conda with the following commands:

```
conda env create --name <env_name> -f environment.yml
conda activate <env_name>
```

## scripts: ## 
- `download_words.py`: downloads the hungarian words woth specified lengths from https://hu.wiktionary.org/wiki/Index:Magyar and stores them in a directory tree. The downloaded words are stored in the _words_ directory.
- `changed_letter.py`: finds word pairs with specified length differ only in one character.
- `extra_letter_at_end.py`: finds word pairs where the second word is composed by adding an extra letter to the end of the first one. The firs word has a specified length.
- `extra_letter_in_between.py`: finds word pairs where the second one is composed from the first one by adding a character to it. The extra character is not the first nor the last character. The first word has a specified length.
- `switched_neighboring_letters.py`: finds word pairs with specified length which are almost the same only 2 neighboring characters are switched.
- `common_funcs.py`: some commonly used functions.

The outputs of the scripts are stored in the _output_ directory in .csv files.

The scripts are currently written for Hungarian language, however with slight changes it can be used for any language. (For instance the url to download the words from and the abc has to be changed.)

## Examples ##
These are the commands for Ubuntu terminal use.

- Download hungarian words with lengths [3, 4, 5]: `python download_words.py --lengths 3 4 5`
- Find word pairs with length=6 differ only in one character: `python changed_letter.py --length 6`
- Find word pairs where the second word is composed by adding an extra letter to the end of the first one. The first one has length=6.: `python extra_letter_at_end.py --length 6`
- Find word pairs where the second one is composed from the first one by adding a character to it. The extra character is not the first nor the last character. The first word has length=6: `python extra_letter_in_between.py --length 6`
- Find word pairs with length=6 which are almost the same only 2 neighboring characters are switched: `python switched_neighboring_letters.py --length 6`
