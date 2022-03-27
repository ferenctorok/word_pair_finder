from sys import warnoptions
from common_funcs import read_words_from_file, dump_words
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as msgbox
import os
import random


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

        self._searchOutDir = OUTROOTDIR
        self._mixOutDir = OUTROOTDIR
        self._mixFileList = []
        self._mixOutPath = ""

        self._window = tk.Tk()
        self._window.title("Szó kereső")

        self._initRow()

        # search function widgets
        self._searchLabel = tk.Label(text="Pipáld ki, melyik betűk lehetnek a szavakban!")
        self._searchLabel.grid(row=self._nextRow(), column = 0, columnspan=7, pady=10)

        self._checkBoxes = self._setUpCheckboxes()

        self._everyLetterState = tk.IntVar()
        self._check = tk.Checkbutton(
            text="Tartalmazza az összes betűt",
            variable=self._everyLetterState
        )
        self._check.grid(row=self._nextRow(), column=0, columnspan=7, pady=10)

        self._searchOutFileButton = tk.Button(text="Mentés helye")
        self._searchOutFileButton.bind("<Button-1>", self._searchOutFileButtonEventHandler)
        self._searchOutFileButton.grid(row=self._nextRow(), column=0, columnspan=2)

        self._searchOutFileTextVariable = tk.StringVar()
        self._searchOutFileTextVariable.set(self._searchOutDir)
        self._searchOutFileLabel = tk.Label(textvariable=self._searchOutFileTextVariable, justify="left")
        self._searchOutFileLabel.grid(row=self._currentRow(), column=2, columnspan=5, pady=10)

        self._searchButton = tk.Button(text="Keresés")
        self._searchButton.bind("<Button-1>", self._searchButtonEventHandler)
        self._searchButton.grid(row=self._nextRow(), column=0, columnspan=7)

        # mix function widget
        separator = ttk.Separator(self._window, orient="horizontal")
        separator.grid(row=self._nextRow(), column=0, columnspan=7, sticky="ew", pady=20)

        self._mixLabel = tk.Label(text="Válaszd ki melyik filet vagy fileokat szeretnéd összekeverni!")
        self._mixLabel.grid(row=self._nextRow(), column=0, columnspan=7)

        self._mixInFileButton = tk.Button(text="Megnyitás")
        self._mixInFileButton.bind("<Button-1>", self._mixInFileButtonEventHandler)
        self._mixInFileButton.grid(row=self._nextRow(), column=0, columnspan=2)

        self._mixInFileTextVariable = tk.StringVar()
        self._mixInFileTextVariable.set("Jelenleg nincs file kiválasztva.")
        self._mixInFileLabel = tk.Label(textvariable=self._mixInFileTextVariable, justify="left")
        self._mixInFileLabel.grid(row=self._currentRow(), column=2, columnspan=5, pady=10)

        self._mixOutFileButton = tk.Button(text="Mentés helye")
        self._mixOutFileButton.bind("<Button-1>", self._mixOutFileButtonEventHandler)
        self._mixOutFileButton.grid(row=self._nextRow(), column=0, columnspan=2)

        self._mixOutFileTextVariable = tk.StringVar()
        self._mixOutFileTextVariable.set("")
        self._mixOutFileLabel = tk.Label(textvariable=self._mixOutFileTextVariable, justify="left")
        self._mixOutFileLabel.grid(row=self._currentRow(), column=2, columnspan=5, pady=10)

        self._mixButton = tk.Button(text="Keverés")
        self._mixButton.bind("<Button-1>", self._mixButtonEventHandler)
        self._mixButton.grid(row=self._nextRow(), column=0, columnspan=7)

        self._window.mainloop()

    def _initRow(self):
        """Initializes the row counter to -1. Hence, the first time self._nextRow is called, it will return 0."""
        self._row = -1

    def _nextRow(self):
        """It increments the current row count by one and returns the value."""
        self._row += 1
        return self._row

    def _currentRow(self):
        """Returns the actual row."""
        return self._row

    def _setUpCheckboxes(self) -> dict:
        """Sets up the checkboxes."""

        checkBoxes = {}
        col = 0
        row = self._nextRow()
        for letter in ABC:
            var = tk.IntVar()
            box = tk.Checkbutton(text=letter, variable=var)
            box.grid(row=row, column=col, sticky='w')
            checkBoxes.update({box: (var, letter)})

            col += 1
            if col >= 7:
                col = 0
                if letter is not ABC[-1]:
                    row = self._nextRow()
        
        return checkBoxes

    def _getLettersFromCheckBoxes(self) -> list:
        """returns the list of letters which were ticked in in the checkboxes."""

        letters = []
        for (val, letter) in self._checkBoxes.values():
            if val.get():
                letters.append(letter)

        return letters

    def _searchButtonEventHandler(self, event):
        """Handles the event when the search button is pressed."""
        # lettersList = self._textIn.get().split()
        lettersList = self._getLettersFromCheckBoxes()

        if (self._everyLetterState.get()):
            success = findWordsWithLetters(lettersList, self._searchOutDir, mustContainEveryLetter=True)
        else:
            success = findWordsWithLetters(lettersList, self._searchOutDir)

        if success:
            msgbox.showinfo(
                title="Szó keresés sikeres!",
                message="a talált szavak a {} mappába lettek mentve.".format(self._searchOutDir)
            )
        else:
            msgbox.showerror(
                title="Sikertelen keresés!",
                message="Nem található szó a megadott betűkkel: \n{}".format(lettersList) 
            )
        
        # for releasing the button. Otherwise it remains pressed always.
        return "break"

    def _mixButtonEventHandler(self, event):
        """Handles the event when the mix button is pressed."""

        if (self._mixFileList):
            mixWords(self._mixFileList, self._mixOutPath)
            
            msgbox.showinfo(
                title="Szó keverés sikeres!",
                message="a megkevert szavak a {} fileba lettek mentve.".format(self._mixOutPath)
            )
        else:
            msgbox.showerror(
                title="Sikertelen keverés!",
                message="Nincsen megadva file keverésre.".format(lettersList)
            )

        # for releasing the button. Otherwise it remains pressed always.
        return "break"

    def _mixInFileButtonEventHandler(self, event):
        """Handles the event when the file opening button is pressed."""

        filenames = list(fd.askopenfilenames(
            initialdir=self._mixOutDir,
            filetypes=[("Text Files", ".txt")]
        ))

        if not filenames:
            return "break"

        text = "\n".join(filenames)
        self._mixInFileTextVariable.set(text)

        self._mixOutDir = os.path.dirname(filenames[0])
        self._mixFileList = filenames

        # for releasing the button. Otherwise it remains pressed always.
        return "break"

    def _mixOutFileButtonEventHandler(self, event):
        """Handles the event when the file opening button is pressed."""

        self._mixOutPath = fd.asksaveasfilename(
            initialdir=self._mixOutDir,
            filetypes=[("Text Files", ".txt")]
        )
        
        if self._mixOutPath[-4:] != ".txt":
            self._mixOutPath += ".txt"
        
        self._mixOutFileTextVariable.set(self._mixOutPath)

        # for releasing the button. Otherwise it remains pressed always.
        return "break"

    def _searchOutFileButtonEventHandler(self, event):
        """Handles the event when the file opening button is pressed."""

        self._searchOutDir = fd.askdirectory(
            initialdir=self._searchOutDir
        )

        self._searchOutFileTextVariable.set(self._searchOutDir)

        # for releasing the button. Otherwise it remains pressed always.
        return "break"


def findWordsWithLetters(letters: list, outDir: str, mustContainEveryLetter: bool = False) -> bool:
    """Searches for words which contain only the letters given in
    the list letters. If mustContainEveryLetter is true, the words should contain all of the letters.

    because of the letters which are written with multiple characters,
    it is not possible to use the set() method to check the correspondence.
    This is why rather for loops are used.
    """

    if not letters:
        return False
    
    outDirBasename = "_".join(letters) + "_every" if mustContainEveryLetter else "_".join(letters)
    outDirTotal = os.path.join(outDir, outDirBasename)
    if not os.path.exists(outDirTotal):
        os.makedirs(outDirTotal)

    longestString = max([len(s) for s in letters])

    success = False

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
            outFile = os.path.join(outDirTotal, wordLength + ".txt")
            dump_words(goodWords, outFile)
            success = True

    return success


def checkIfOnlyContainsAllowedChars(word: str, letters: list, longestString: str) -> bool:
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


def mixWords(fileNameList: list, outFile: str = "") -> None:
    """Reads in the words from the files, mixes their order randomly and dumps
    them in an output file in the same directory
    
    args:
        filenames: [list], the list of files to read from.
    """

    currentDir = os.path.dirname(fileNameList[0])
    wordLengthList = []
    wordList = []

    for filePath in fileNameList:
        fileBasename = os.path.basename(filePath)
        wordLength = int(fileBasename.split('.')[0])
        wordLengthList.append(wordLength)

        with open(filePath, 'r', encoding="utf8") as fp:
            wordList += fp.read().splitlines()

    random.shuffle(wordList)

    if not outFile:
        wordLengthList.sort()
        outFileName = "mix_" + "_".join([str(length) for length in wordLengthList])
        outFileBase = outFileName + ".txt"
        outFile = os.path.join(currentDir, outFileBase)

    dump_words(wordList, outFile)


if __name__ == "__main__":
    gui = GUI()
