from collections import Counter
from typing import Dict, List, Tuple

import tqdm

from parsing.chapter import Chapter
from parsing.metadata import BookMetadata
from parsing.parasha import Parasha
from parsing.verse import TaamSequenceResult, Verse
from utils.text_parsing_utils import TextParsingUtils


class Book:
    """
    A Book is a sequence of chapters.
    """

    @staticmethod
    def _extract_parshiot(
        chapters: List[Chapter], metadata: BookMetadata
    ) -> List[Parasha]:
        """
        Extract the Parshiot from the sequence of chapters and the
        book's metadata.

        :param chapters: The sequence of chapters.
        :param metadata: The metadata of the book (with information about where
                         aliyot and parshiot start and end).
        :return: A list of parshiot objects that make up this book.
        """
        return [
            Parasha.from_chapters(metadata, chapters) for metadata in metadata.parshiot
        ]

    def __init__(self, name: str, chapters: List[Chapter], metadata: BookMetadata):
        self.name = name
        self._chapters = chapters
        self._parshiot = Book._extract_parshiot(chapters, metadata)
        self._verses = [verse for chapter in chapters for verse in chapter.verses]

    def __repr__(self) -> str:
        parts = []
        for chapter in self.chapters:
            parts.append(f"Chapter {chapter._idx}\n")
            parts.append(str(chapter))
            parts.append("\n")
        return "".join(parts)

    @classmethod
    def chapters_from_string(cls, s: str) -> "Book":
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

        metadata = BookMetadata(book_name)
        return Book(book_name, chapters, metadata)

    @classmethod
    def from_text_file(cls, file_path: str) -> "Book":
        """
        Parse a book from a text file.

        :param file_path: The path to the text file.
        :return: A Book object.
        """
        with open(file_path, "r", encoding="utf-8") as book:
            lines = book.read()
            return cls.chapters_from_string(lines)

    @property
    def parshiot(self):
        """
        Get the Parshiot in the Book.

        :return: The Parshiot in the Book.
        """
        return self._parshiot

    @property
    def chapters(self):
        """
        Get the chapters in the Book.

        :return: The chapters in the Book.
        """
        return self._chapters

    @property
    def verses(self):
        """
        Get the verses in the Book.

        :return: The verses in the Book.
        """
        return self._verses

    @property
    def taamim(self):
        """
        Get the Taamim in the Book.

        :return: The Taamim in the Book.
        """
        return [taam for verse in self.verses for taam in verse.taamim]

    @property
    def taamim_without_meshartim(self):
        """
        Get the Taamim in the Book without the Meshartim.

        :return: The Taamim in the Book without the Meshartim.
        """
        return [
            taam for verse in self.verses for taam in verse.taamim_without_meshartim
        ]

    def find_verses_with_taam_sequence(
        self, taam_sequence: List[str], include_meshartim: bool = True
    ) -> Dict[str, List[List[Tuple[Verse, TaamSequenceResult]]]]:
        """
        Find verses with a sequence of Taamim broken down by parasha and aliyah.

        :param taam_sequence: The taam sequence to find.
        :param include_meshartim: Whether to include Meshartim in the search, defaults to True
        :return: A dictionary mapping parashiot to a list of lists of verses. (The elements
                 of the outer list are the aliyot, and the elements of the inner list are
                 the verses in the aliyah that contain the sequence.)
        """
        by_parasha = {}
        for parasha in self.parshiot:
            verses_by_aliyah = parasha.find_verses_with_taam_sequence(
                taam_sequence, include_meshartim
            )
            if verses_by_aliyah:
                by_parasha[parasha.name] = verses_by_aliyah
        return by_parasha

    def count_n_taam_sequences(
        self, n: int, include_meshartim: bool = True
    ) -> Dict[tuple, int]:
        """
        Count the number of n-Taam sequences in the Book.

        :param n: The length of the Taam sequences to count.
        :param include_meshartim: Whether or not to include Meshartim when looking
                                  for sequences, defaults to True
        :return: The sequence (tuple) mapped to the number of occurrences of that
                 sequence in the Book.
        """
        taam_sequence_counts = Counter()
        for parasha in self.parshiot:
            taam_sequence_counts += parasha.count_n_taam_sequences(n, include_meshartim)
        return taam_sequence_counts
