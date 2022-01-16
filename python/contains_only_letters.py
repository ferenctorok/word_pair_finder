import csv
from argparse import ArgumentParser
from common_funcs import read_words_from_file, get_shortened_list_by_index
import tkinter as tk
import os


if __name__ == "__main__":
    OUTROOTDIR = os.path.join("output", "contains_only_letters")
    WORDSDIR = os.path.join("words")


class GUI:
    """Class that contains the gui and its methods."""

    def __init__(self):
        """creates the gui for the application."""

        self._window = tk.Tk()

        self._label = tk.Label(text="Add meg a betűket szóközzel elválasztva!")
        self._label.pack()

        self._textIn = tk.Entry()
        self._textIn.pack()

        self._checkState = tk.IntVar()
        self._check = tk.Checkbutton(
            text="Tartalmazzák az összes betűt",
            variable=self._checkState
        )
        self._check.pack()

        self._button = tk.Button(text="Keresés")
        self._button.bind("<Button-1>", self._buttonEventHandler)
        self._button.pack()

        self._window.mainloop()

    def _buttonEventHandler(self, event):
        """Handles the event when the button is pushed."""
        lettersList = self._textIn.get().split()

        if (self._checkState.get()):
            searchWordsEveryLetter(lettersList)
        else:
            searchWordsSimple(lettersList)

def searchWordsEveryLetter(letters):
    """Searches for words which contain only the letters given in
    the list letters and contain all of them.

    because of the letters which are written with multiple characters,
    it is not possible to use the set() method to check the correspondence.
    This is why rather for loops are used.
    """

    longestString = max([len(s) for s in letters])

    outDir = os.path.join(OUTROOTDIR, "_".join(letters) + "_every")
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for inDir in os.listdir(WORDSDIR):
        currentInDir = os.path.join(WORDSDIR, inDir)
        currentOutDir = os.path.join(outDir, inDir)
        if not os.path.exists(currentOutDir):
            os.makedirs(currentOutDir)

        for fileName in os.listdir(currentInDir):
            initLetter = fileName.split('.')[0]
            if initLetter not in letters:
                continue

            wordList = read_words_from_file(currentInDir, fileName)
            goodWords = []

            for word in wordList:
                okFlag = checkIfOnlyContainsAllowedChars(word, letters, longestString)

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
                outFile = os.path.join(currentOutDir, fileName)
                with open(outFile, 'w') as fp:
                    for word in goodWords:
                        fp.writelines(word + "\n")

        # deleting the output dir if it does not contain anything:
        if not os.listdir(currentOutDir):
            os.rmdir(currentOutDir)


def searchWordsSimple(letters):
    """Searches for words which contain only letters given in letters"""

    longestString = max([len(s) for s in letters])

    outDir = os.path.join(OUTROOTDIR, "_".join(letters))
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for inDir in os.listdir(WORDSDIR):
        currentInDir = os.path.join(WORDSDIR, inDir)
        currentOutDir = os.path.join(outDir, inDir)
        if not os.path.exists(currentOutDir):
            os.makedirs(currentOutDir)

        for fileName in os.listdir(currentInDir):
            initLetter = fileName.split('.')[0]
            if initLetter not in letters:
                continue

            wordList = read_words_from_file(currentInDir, fileName)
            goodWords = []

            for word in wordList:
                if checkIfOnlyContainsAllowedChars(word, letters, longestString):
                    goodWords.append(word)

            if goodWords:
                outFile = os.path.join(currentOutDir, fileName)
                with open(outFile, 'w') as fp:
                    for word in goodWords:
                        fp.writelines(word  + "\n")

        # deleting the output dir if it does not contain anything:
        if not os.listdir(currentOutDir):
            os.rmdir(currentOutDir)


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
