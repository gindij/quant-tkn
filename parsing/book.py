from collections import defaultdict
from typing import Dict, List

import tqdm

from parsing.chapter import Chapter
from parsing.verse import Verse
from parsing.word import Word
from utils.text_parsing_utils import TextParsingUtils


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
        self._nequdot = [niqud for letter in self._letters for niqud in letter.nequdot]
        self._taamim = [taam for word in self._words for taam in word.taamim]
        self._taamim_without_meshartim = [
            taam for word in self._words for taam in word.taamim_without_meshartim
        ]

    def __repr__(self) -> str:
        parts = []
        for chapter in self.chapters:
            parts.append(f"Chapter {chapter.idx}\n")
            parts.append(str(chapter))
            parts.append("\n")
        return "".join(parts)

    @classmethod
    def from_string(cls, s: str) -> "Book":
        """
        Parse a book from a string.

        :param s: The string representation of the Book.
        :return: A Book object.
        """
        chapters = []
        book_name = None
        for line in tqdm.tqdm(s.split("\n")):
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

    @classmethod
    def from_text_file(cls, file_path: str) -> "Book":
        """
        Parse a book from a text file.

        :param file_path: The path to the text file.
        :return: A Book object.
        """
        with open(file_path, "r", encoding="utf-8") as book:
            lines = book.read()
            return cls.from_string(lines)

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
    def nequdot(self):
        """
        Get the nequdot in the Book.

        :return: The nequdot in the Book.
        """
        return self._nequdot

    @property
    def taamim(self):
        """
        Get the taamim in the Book.

        :return: The taamim in the Book.
        """
        return self._taamim

    @property
    def taamim_without_meshartim(self):
        """
        Get the taamim in the Book without the meshartim.

        :return: The taamim in the Book without the meshartim.
        """
        return self._taamim_without_meshartim

    def find_verses_with_taam_sequence(
        self, taam_sequence: List[str], include_meshartim: bool
    ) -> List[Verse]:
        """
        Find all verses containing a specific Taam.

        :param taam_name: The name of the Taam.
        :param include_meshartim: Whether to include taame mesharet when looking for verses containing a sequence.
        :return: A list of Verses containing the Taam.
        """
        verses = []
        for verse in tqdm.tqdm(self.verses):
            if verse.has_taam_sequence(taam_sequence, include_meshartim):
                verses.append(verse)
        return verses

    def count_n_taam_sequences(
        self, n: int, include_meshartim: bool = True
    ) -> Dict[tuple, int]:
        """
        Collect all occurring n-Taam sequences in a book.

        :param n: The length of the taam sequence to look for.
        :param include_meshartim: Whether to include taame mesharet in the sequences.
        :return: A list of n-Taam sequences that occur in this book.
        """
        taam_sequence_counts = defaultdict(int)
        for verse in tqdm.tqdm(self.verses):
            taamim = (
                verse.taamim if include_meshartim else verse.taamim_without_meshartim
            )
            for i in range(len(taamim) - n + 1):
                taam_sequence = []
                for j in range(n):
                    if i + j < len(taamim):
                        taam_sequence.append(taamim[i + j].name)
                if len(taam_sequence) == n:
                    taam_sequence_counts[tuple(taam_sequence)] += 1
        return taam_sequence_counts
