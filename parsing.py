from collections import namedtuple, OrderedDict, defaultdict
import pprint
from typing import List, Optional, Dict
import tqdm


LRE = "\u202A"
RLE = "\u202B"
PDF = "\u202C"
SKIP_SEQUENCE = "xxxx"

VERSE_LINE_START_SYMBOL = RLE

LETTERS = "־אבגדהוזחטיכלמנסעפצקרשתךםןףץ"
TAAMIM = {
    "\u0591": "atnah",
    "\u0592": "segolta",
    "\u0593": "shalshelet",
    "\u0594": "zaqef_qaton",
    "\u0595": "zaqef_gadol",
    "\u0596": "tarha",
    "\u0597": "ravia",
    "\u0598": "zarqa",
    "\u0599": "pashta",
    "\u059A": "yetiv",
    "\u059B": "tevir",
    "\u059C": "gerish",
    "\u059E": "shene_gerishin",
    "\u059F": "karne_farah",
    "\u05A0": "tarsa",
    "\u05A1": "pazer_gadol",
    "\u05A2": "yareah_ben_yomo",
    "\u05A3": "shofar_holekh",
    "\u05A4": "shofar_mehupakh",
    "\u05A5": "maarikh",
    "\u05A6": "tere_taame",
    "\u05A7": "darga",
    "\u05A8": "qadma",
    "\u0599\u0599": "tere_qadmin",
    "\u05A9": "talsha",
    "\u05AA": "yareah_ben_yomo",
    "\u05AE": "zarqa",
    "\u05BD": "maamid",
    "\u05C0": "paseq",
    "\u05C3": "sof_passuq",
}
TAAMIM_SYMBOLS = {v: k for k, v in TAAMIM.items()}
NEKUDOT = {
    "\u05B0": "shva",
    "\u05B1": "hataf_segol",
    "\u05B2": "hataf_patah",
    "\u05B3": "hataf_qamats",
    "\u05B4": "hiriq",
    "\u05B5": "tsere",
    "\u05B6": "segol",
    "\u05B7": "patah",
    "\u05B8": "qamats",
    "\u05B9": "holam_haser",
    "\u05BB": "qubuts",
    "\u05BC": "dagesh",
    "\u05C1": "shin_dot",
    "\u05C2": "sin_dot",
    "\u05C4": "upper_dot",
}
NEKUDOT_SYMBOLS = {v: k for k, v in NEKUDOT.items()}


class TextParsingUtils:
    """
    Utility functions for parsing text. These functions are used to parse the text files containing the Tanakh.
    """

    @staticmethod
    def is_line_start_of_verse(line: str) -> bool:
        """
        Check if a line is the start of a verse.

        :param line: The line to check.
        :return: True if the line is the start of a verse, False otherwise.
        """
        return line.startswith(VERSE_LINE_START_SYMBOL)

    @staticmethod
    def is_line_start_of_chapter(line: str) -> bool:
        """
        Check if a line is the start of a chapter.

        :param line: The line to check.
        :return: True if the line is the start of a chapter, False otherwise.
        """
        return "Chapter" in line

    @staticmethod
    def is_line_start_of_book(line: str) -> bool:
        """
        Check if a line is the start of a book.

        :param line: The line to check.
        :return: True if the line is the start of a book, False otherwise.
        """
        return "chapters" in line and "verses" in line and "End of" not in line

    @staticmethod
    def extract_chapter_idx(line: str) -> int:
        """
        Extract the chapter index from a line.

        :param line: The chapter specification line.
        :return: The chapter index.
        """
        return int(line.split()[2])

    @staticmethod
    def extract_verse_idx(line: str) -> int:
        """
        Extract the verse index from a line.

        :param line: The verse specification line.
        :return: The verse index.
        """
        return int(line.split()[1])

    @staticmethod
    def extract_book_name(line: str) -> str:
        """
        Extract the book name from a line.

        :param line: The verse specification line.
        :return: The book name.
        """
        return line.split()[1]


class Nikkud:
    """
    A Nikkud is a vowel symbol in the Hebrew Bible.
    """

    def __init__(self, name: str):
        self.name = name
        self.symbol = NEKUDOT_SYMBOLS[name]

    def __repr__(self):
        return self.symbol


class Taam:
    """
    A Taam is a trope symbol in the Hebrew Bible.
    """

    def __init__(self, name: str):
        self.name = name
        self.symbol = TAAMIM_SYMBOLS[name]

    def __repr__(self):
        return self.symbol


class Letter:
    """
    A Letter is a character in the Hebrew alphabet with a Taam and possibly a Dagesh.
    """

    def __init__(
        self,
        letter: str,
        taamim: Optional[List[Taam]] = None,
        nekudot: Optional[List[Nikkud]] = None,
    ):
        if nekudot is None:
            nekudot = []

        if taamim is None:
            taamim = []

        self._letter = letter
        self._taamim = taamim
        self._nekudot = nekudot

    @property
    def taamim(self):
        """
        Get the Taamim in the Letter.

        :return: The Taamim in the Letter.
        """
        return [taam for taam in self._taamim if taam.name != "maamid"]

    @property
    def nekudot(self):
        """
        Get the Nikkud in the Letter.

        :return: The Nikkud in the Letter.
        """
        return self._nekudot

    @property
    def letter(self):
        """
        Get the letter.

        :return: The letter.
        """
        return self._letter

    def add_taam(self, taam: Taam):
        """
        Add a Taam to the Letter.

        :param taam: The Taam to add.
        """
        self._taamim.append(taam)

    def add_nikkud(self, nikkud: Nikkud):
        """
        Add a vowel (nikkud) to the Letter.

        :param nikkud: The Nikkud to add.
        """
        self._nekudot.append(nikkud)

    def has_taam(self, taam_name: str) -> bool:
        """
        Check if the Letter has a specific Taam.

        :param taam_name: The name of the Taam.
        :return: True if the Letter has the Taam, False otherwise.
        """
        return any(taam.name == taam_name for taam in self.taamim)

    def rename_taam(self, old_name: str, new_name: str) -> bool:
        """
        Rename a Taam.

        :param old_name: The current name of the Taam.
        :param new_name: The new name of the Taam.
        :return: True if the Taam was renamed, False otherwise.
        """
        for taam in self.taamim:
            if taam.name == old_name:
                taam.name = new_name
                return True
        return False

    def __repr__(self) -> str:
        taamim = "".join([taam.symbol for taam in self.taamim])
        nekudot = "".join([nikkud.symbol for nikkud in self.nekudot])
        return f"{self.letter}{nekudot}{taamim}"


class Word:
    """
    A Word is a sequence of letters.
    """

    def __init__(self, letters: List[Letter]):
        self._letters = letters
        self._taamim = [taam for letter in self._letters for taam in letter.taamim]
        self._nekudot = [
            nikkud for letter in self._letters for nikkud in letter.nekudot
        ]

    @property
    def letters(self):
        """
        Get the letters in the Word.

        :return: The letters in the Word.
        """
        return self._letters

    @property
    def taamim(self):
        """
        Get the taamim in the Word.

        :return: The taamim in the Word.
        """
        taamim = self._taamim

        for i in range(len(taamim) - 1):
            # if there are two qadma in a row, replace the two with a single
            # taam called tere_qadmin
            if taamim[i].name == "pashta" and taamim[i + 1].name == "pashta":
                taamim[i] = Taam("tere_qadmin")
                taamim.pop(i + 1)
                break

        return taamim

    @property
    def nekudot(self):
        """
        Get the nekudot in the Word.

        :return: The nekudot in the Word.
        """
        return self._nekudot

    def has_taam(self, taam_name: str) -> bool:
        """
        Check if the Word contains a Taam.

        :param taam_name: The name of the Taam.
        :return: True if the Word contains the Taam, False otherwise.
        """
        return any(taam.name == taam_name for taam in self._taamim)

    def rename_taam(self, old_name: str, new_name: str) -> bool:
        """
        Rename a Taam.

        :param old_name: The current name of the Taam.
        :param new_name: The new name of the Taam.
        :return: True if the Taam was renamed, False otherwise.
        """
        for letter in self._letters:
            if letter.rename_taam(old_name, new_name):
                return True
        return False

    def is_setumah(self) -> bool:
        """
        Check if the Word is a Setumah (a single ס).

        :return: True if the Word is a Setumah, False otherwise.
        """
        return len(self) == 1 and self.letters[0].letter == "ס"

    def is_petuhah(self) -> bool:
        """
        Check if the Word is a Petuhah (a single פ).

        :return: True if the Word is a Petuhah, False otherwise.
        """
        return len(self) == 1 and self.letters[0].letter == "פ"

    def __repr__(self) -> str:
        return "".join([str(letter) for letter in self.letters])

    def __len__(self) -> int:
        return len(self.letters)


class Verse:
    """
    A Verse is a sequence of words.
    """

    def __init__(self, idx: int, words: List[Word]):
        self.idx = idx
        self._words = words
        self._letters = [letter for word in words for letter in word.letters]
        self._taamim = [taam for word in words for taam in word.taamim]
        self._nekudot = [
            nikkud for letter in self._letters for nikkud in letter.nekudot
        ]

    def __repr__(self) -> str:
        return LRE + " ".join([str(word) for word in self._words]) + PDF

    @classmethod
    def from_string(cls, idx: int, s: str) -> "Verse":
        """
        Parse a pasuk from a string.

        :param idx: The index of the Verse (within a Chapter).
        :param s: The string representation of the Verse.
        :return: A Verse object.
        """
        words = []
        for word in s.split():
            letters = []
            for i, char in enumerate(word):
                if char in LETTERS:
                    letters.append(Letter(char))
                elif char in TAAMIM:
                    if len(letters) == 0:
                        if char == TAAMIM_SYMBOLS["paseq"]:
                            words[-1].letters[-1].add_taam(Taam(TAAMIM[char]))
                    else:
                        letters[-1].add_taam(Taam(TAAMIM[char]))
                elif char in NEKUDOT:
                    letters[-1].add_nikkud(Nikkud(NEKUDOT[char]))
            words.append(Word(letters))

        # change any pashtas in the middle of a word to kadmas
        for wd in words:
            for i, letter in enumerate(wd.letters):
                no_more_pashtas = not any(
                    wd.letters[j].has_taam("pashta")
                    for j in range(i + 1, len(wd.letters))
                )
                if letter.has_taam("pashta") and i < len(wd) - 1 and no_more_pashtas:
                    letter.rename_taam("pashta", "qadma")

        # change any qadmas that are followed by a qadma to azlas
        for wd1, wd2 in zip(words, words[1:]):
            if wd1.has_taam("qadma") and wd2.has_taam("gerish"):
                wd1.rename_taam("qadma", "azla")
            elif wd1.has_taam("qadma") and wd1.has_taam("gerish"):
                wd1.rename_taam("qadma", "azla")

        # make sure every verse ends with a sof_passuq
        while len(words[-1]) == 0:
            words.pop()

        return cls(idx, words)

    @property
    def letters(self):
        """
        Get the letters in the Verse.

        :return: The letters in the Verse.
        """
        return self._letters

    @property
    def taamim(self):
        """
        Get the taamim in the Verse.

        :return: The taamim in the Verse.
        """
        return self._taamim

    @property
    def nekudot(self):
        """
        Get the nekudot in the Verse.

        :return: The nekudot in the Verse.
        """
        return self._nekudot

    @property
    def words(self):
        """
        Get the words in the Verse.

        :return: The words in the Verse.
        """
        return self._words

    def has_taam(self, taam_name: str) -> bool:
        """
        Check if the Verse contains a Taam.

        :param taam_name: The name of the Taam.
        :return: True if the Verse contains the Taam, False otherwise.
        """
        return any(word.has_taam(taam_name) for word in self._words)

    def has_taam_sequence(self, taam_sequence: List[str]) -> bool:
        """
        Check if the Verse contains a sequence of Taamim. We exclude maamids.

        :param taam_sequence: The sequence of Taamim.
        :return: True if the Verse contains the sequence, False otherwise.
        """
        all_taamim = [
            taam
            for word in self._words
            for taam in word.taamim
            if taam.name != "maamid"
        ]
        for i in range(len(all_taamim) - len(taam_sequence) + 1):
            if all(
                all_taamim[i + j].name == taam_sequence[j]
                for j in range(len(taam_sequence))
            ):
                return True
        return False

    def count_taam(self, taam_name: str) -> int:
        """
        Count the number of occurrences of a Taam in the Verse.

        :param taam_name: The name of the Taam.
        :return: The number of occurrences of the Taam.
        """
        return sum(word.has_taam(taam_name) for word in self._words)


class Chapter:
    """
    A Chapter is a sequence of verses.
    """

    def __init__(self, idx: int, verses: List[Verse]):
        self.idx = idx
        self._verses = verses

    def __repr__(self) -> str:
        return "\n".join(
            [f"{self.idx}:{verse.idx} " + str(verse) for verse in self.verses]
        )

    @property
    def verses(self):
        """
        Get the verses in the Chapter.

        :return: The verses in the Chapter.
        """
        return self._verses

    def add_verse(self, verse: Verse):
        """
        Add a verse to the Chapter.

        :param verse: The verse to add.
        """
        self._verses.append(verse)

    def count_taam(self, taam_name: str) -> int:
        """
        Count the number of occurrences of a Taam in the Chapter.

        :param taam_name: The name of the Taam.
        :return: The number of occurrences of the Taam.
        """
        return sum(verse.count_taam(taam_name) for verse in self.verses)


class Book:
    """
    A Book is a sequence of chapters.
    """

    def __init__(self, name: str, chapters: List[Chapter]):
        self.name = name
        self._chapters = chapters
        self._verses = [verse for chapter in chapters for verse in chapter.verses]
        self._words = [word for verse in self._verses for word in verse._words]
        self._letters = [letter for word in self._words for letter in word.letters]
        self._nekudot = [
            nikkud for letter in self._letters for nikkud in letter.nekudot
        ]
        self._taamim = [taam for word in self._words for taam in word.taamim]

    def __repr__(self) -> str:
        parts = []
        for chapter in self.chapters:
            parts.append(f"Chapter {chapter.idx}\n")
            parts.append(str(chapter))
            parts.append("\n")
        return "".join(parts)

    @classmethod
    def from_text_file(cls, file_path: str) -> "Book":
        """
        Parse a book from a text file.

        :param file_path: The path to the text file.
        :return: A Book object.
        """
        with open(file_path, "r", encoding="utf-8") as book:
            chapters = []
            lines = book.readlines()
            book_name = None
            for line in tqdm.tqdm(lines):
                # LRE symbol indicates the beginning of a verse
                if TextParsingUtils.is_line_start_of_verse(line):
                    verse_idx = TextParsingUtils.extract_verse_idx(line)
                    verse = Verse.from_string(verse_idx, line)
                    chapters[-1].add_verse(verse)
                elif TextParsingUtils.is_line_start_of_chapter(line):
                    chapter_idx = TextParsingUtils.extract_chapter_idx(line)
                    chapters.append(Chapter(chapter_idx, []))
                elif TextParsingUtils.is_line_start_of_book(line):
                    book_name = TextParsingUtils.extract_book_name(line)
        return Book(book_name, chapters)

    @property
    def letters(self):
        """
        Get the letters in the Book.

        :return: The letters in the Book.
        """
        return self._letters

    @property
    def words(self):
        """
        Get the words in the Book.

        :return: The words in the Book.
        """
        return self._words

    @property
    def verses(self):
        """
        Get the verses in the Book.

        :return: The verses in the Book.
        """
        return self._verses

    @property
    def chapters(self):
        """
        Get the chapters in the Book.

        :return: The chapters in the Book.
        """
        return self._chapters

    @property
    def nekudot(self):
        """
        Get the nekudot in the Book.

        :return: The nekudot in the Book.
        """
        return self._nekudot

    @property
    def taamim(self):
        """
        Get the taamim in the Book.

        :return: The taamim in the Book.
        """
        return self._taamim

    def find_verses_with_taam(self, taam_name: str) -> List[Verse]:
        """
        Find all verses containing a specific Taam.

        :param taam_name: The name of the Taam.
        :return: A list of Verses containing the Taam.
        """
        verses = []
        for verse in tqdm.tqdm(self.verses):
            if verse.has_taam(taam_name):
                verses.append(verse)
        return verses

    def find_verses_with_taam_sequence(self, taam_sequence: List[str]) -> List[Verse]:
        """
        Find all verses containing a specific Taam.

        :param taam_name: The name of the Taam.
        :return: A list of Verses containing the Taam.
        """
        verses = []
        for verse in tqdm.tqdm(self.verses):
            if verse.has_taam_sequence(taam_sequence):
                verses.append(verse)
        return verses

    def find_words_with_taam(self, taam_name: str) -> List[Word]:
        """
        Find all words containing a specific Taam.

        :param taam_name: The name of the Taam.
        :return: A list of Words containing the Taam.
        """
        words = []
        for word in tqdm.tqdm(self.words):
            if any(taam.name == taam_name for taam in word.taamim):
                words.append(word)
                break
        return words

    def find_taam_sequences(self, taam_sequence: List[str]) -> List[Verse]:
        """
        Find all verses containing a sequence of Taamim.

        :param taam_sequence: The sequence of Taamim.
        :return: A list of Verses containing the sequence.
        """
        verses = []
        for verse in tqdm.tqdm(self.verses):
            if verse.has_taam_sequence(taam_sequence):
                verses.append(verse)
        return verses

    def count_n_taam_sequences(self, n: int) -> Dict[tuple, int]:
        """
        Collect all occurring n-Taam sequences in a book.

        :param n: The length of the taam sequence to look for.
        :return: A list of n-Taam sequences that occur in this book.
        """
        taam_sequence_counts = defaultdict(int)
        for verse in tqdm.tqdm(self.verses):
            for i in range(len(verse.taamim) - n + 1):
                taam_sequence = []
                for j in range(n):
                    if i + j < len(verse.taamim):
                        taam_sequence.append(verse.taamim[i + j].name)
                if len(taam_sequence) == n:
                    taam_sequence_counts[tuple(taam_sequence)] += 1
        return taam_sequence_counts
