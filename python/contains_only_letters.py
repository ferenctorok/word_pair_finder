import csv
from argparse import ArgumentParser
from common_funcs import read_words_from_file, get_shortened_list_by_index
import tkinter as tk
import os


OUTROOTDIR = os.path.join("output", "contains_only_letters")
WORDSDIR = os.path.join("words")
ABC = [
    'a', 'á', 'b', 'c', 'cs', 'd', 'dz', 'dzs', 'e', 'é', 'f', 'g', 'gy', 'h', 'i', 'í', 'j', 'k', 'l', 'ly', 'm', 'n',
    'ny', 'o', 'ó', 'ö', 'ő', 'p', 'q', 'r', 's', 'sz', 't', 'ty', 'u', 'ú', 'ü', 'ű', 'v', 'w', 'x', 'y', 'z', 'zs'
]

# Some of the words starting with a letter, like á, are in a different file (a).
# This is why this dict is needed:
LETTER_PAIRS = {'a': 'á', 'i': 'í', 'o': 'ó', 'ü': 'ű'}


class GUI:
    """Class that contains the gui and its methods."""

    def __init__(self):
        """creates the gui for the application."""

        self._window = tk.Tk()
        self._window.title("Szó kereső")

        self._label = tk.Label(text="Pipáld ki, melyik betűk lehetnek a szavakban!")
        self._label.grid(row=0, column = 0, columnspan=7)

        self._checkBoxes = self._setUpCheckboxes()

        self._everyLetterState = tk.IntVar()
        self._check = tk.Checkbutton(
            text="Tartalmazzák az összes betűt",
            variable=self._everyLetterState
        )
        self._check.grid(row=9, column=0, columnspan=7)

        self._button = tk.Button(text="Keresés")
        self._button.bind("<Button-1>", self._buttonEventHandler)
        self._button.grid(row=10, column=0, columnspan=7)

        self._window.mainloop()

    def _setUpCheckboxes(self) -> dict:
        """Sets up the checkboxes."""

        checkBoxes = {}
        colCounter = 0
        rowCounter = 1
        for letter in ABC:
            var = tk.IntVar()
            box = tk.Checkbutton(text=letter, variable=var)
            box.grid(row=rowCounter, column=colCounter)
            checkBoxes.update({box: (var, letter)})

            colCounter += 1
            if colCounter >= 7:
                colCounter = 0
                rowCounter += 1
        
        return checkBoxes

    def _getLettersFromCheckBoxes(self) -> list:
        """returns the list of letters which were ticked in in the checkboxes."""

        letters = []
        for (val, letter) in self._checkBoxes.values():
            if val.get():
                letters.append(letter)

        return letters

    def _buttonEventHandler(self, event):
        """Handles the event when the button is pushed."""
        # lettersList = self._textIn.get().split()
        lettersList = self._getLettersFromCheckBoxes()

        if (self._everyLetterState.get()):
            findWordsWithLetters(lettersList, mustContainEveryLetter=True)
        else:
            findWordsWithLetters(lettersList)

def findWordsWithLetters(letters, mustContainEveryLetter=False):
    """Searches for words which contain only the letters given in
    the list letters. If mustContainEveryLetter is true, the words should contain all of the letters.

    because of the letters which are written with multiple characters,
    it is not possible to use the set() method to check the correspondence.
    This is why rather for loops are used.
    """
    
    outDirBasename = "_".join(letters) + "_every" if mustContainEveryLetter else "_".join(letters)
    outDir = os.path.join(OUTROOTDIR, outDirBasename)
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    longestString = max([len(s) for s in letters])

    for wordLength in os.listdir(WORDSDIR):
        currentInDir = os.path.join(WORDSDIR, wordLength)
        
        goodWords = []

        for fileName in os.listdir(currentInDir):
            initLetter = fileName.split('.')[0]

            if (initLetter not in letters):
                if (initLetter in list(LETTER_PAIRS.keys())):
                    if (LETTER_PAIRS[initLetter] not in letters):
                        continue
                else:
                    continue
                    
            wordList = read_words_from_file(currentInDir, fileName)

            for word in wordList:
                okFlag = checkIfOnlyContainsAllowedChars(word, letters, longestString)

                if mustContainEveryLetter:
                    if not okFlag:
                        continue
                    
                    # checking whether the word contains every letter:
                    for letter in letters:
                        if letter not in word:
                            okFlag = False
                            break
                
                if okFlag:
                    goodWords.append(word)

        if goodWords:
            outFile = os.path.join(outDir, wordLength + ".txt")
            with open(outFile, 'w', encoding="utf8") as fp:
                for word in goodWords:
                    fp.writelines(word + "\n")


def checkIfOnlyContainsAllowedChars(word, letters, longestString):
    """Returns true if the given word only contains characters or strings,
    which are in the list letters. The longestStering argument is the
    length of the longest string in letters.
    """

    i1 = 0
    while (i1 < len(word)):
        okFlag = False
        i2 = i1 + 1

        while ((not okFlag) and
            (i2 <= len(word)) and
            ((i2 - i1) <= longestString)
        ):
            if word[i1: i2] in letters:
                okFlag = True
                i1 = i2
            
            i2 += 1

        if not okFlag:
            break
    
    return okFlag


if __name__ == "__main__":
    gui = GUI()
