from typing import List

import requests

API_BASE_URL = "https://www.sefaria.org/api/v2/raw/index"


class ChapterVerseMetadata:
    """
    Metadata for a chapter-verse pair.
    """

    def __init__(self, metadata_str: str):
        self._chapter_idx, self._verse_idx = [int(x) for x in metadata_str.split(":")]

    @property
    def chapter_idx(self) -> int:
        """
        Gets the integer index of the chapter.

        :return: The integer index of the chapter.
        """
        return self._chapter_idx

    @property
    def verse_idx(self) -> int:
        """
        Gets the integer index of the verse.

        :return: The integer index of the verse.
        """
        return self._verse_idx


class AliyahMetadata:
    """
    Metadata for an aliyah. For each aliyah, we have the starting and ending chapter-verse pairs.
    """

    def __init__(self, aliyah_idx: int, metadata_str: str):

        self._aliyah_idx = aliyah_idx
        full_chapter_verse_str = metadata_str.split()[1].replace("–", "-")

        assert "-" in full_chapter_verse_str, full_chapter_verse_str

        start_chapter_verse_str, end_chapter_verse_str = full_chapter_verse_str.split(
            "-"
        )

        # If the end chapter-verse string does not have a chapter, assume it is the same as the start chapter.
        if len(end_chapter_verse_str.split(":")) == 1:
            end_chapter_verse_str = (
                f"{start_chapter_verse_str.split(':')[0]}:{end_chapter_verse_str}"
            )
        assert len(start_chapter_verse_str.split(":")) == 2, start_chapter_verse_str
        assert len(end_chapter_verse_str.split(":")) == 2, end_chapter_verse_str

        self._start = ChapterVerseMetadata(start_chapter_verse_str)
        self._end = ChapterVerseMetadata(end_chapter_verse_str)

    @property
    def idx(self) -> int:
        """
        Gets the index of the aliyah (0 - 6 inclusive).

        :return: The index of the aliyah.
        """
        return self._aliyah_idx

    @property
    def start_chapter_verse(self) -> ChapterVerseMetadata:
        """
        Gets the starting chapter-verse pair of the aliyah.

        :return: The starting chapter-verse pair of the aliyah.
        """
        return self._start

    @property
    def end_chapter_verse(self) -> ChapterVerseMetadata:
        """
        Gets the ending chapter-verse pair of the aliyah.

        :return: The ending chapter-verse pair of the aliyah.
        """
        return self._end


class ParashaMetadata:
    """
    Metadata for a parasha. For each parasha, we have a list of aliyot
    (aliyah metadata) and the starting and ending chapter-verse pairs
    of the parasha.
    """

    def __init__(self, name: str, aliya_metadata: List[str]):
        self._name = name
        self._aliyot = [
            AliyahMetadata(idx, metadata_str)
            for idx, metadata_str in enumerate(aliya_metadata)
        ]
        self._chapter_verse_start = self._aliyot[0].start_chapter_verse
        self._chapter_verse_end = self._aliyot[-1].end_chapter_verse

    @property
    def name(self) -> str:
        """
        Gets the name of the parasha.

        :return: The name of the parasha.
        """
        return self._name

    @property
    def aliyah_metadata(self) -> List[AliyahMetadata]:
        """
        Gets the metadata of the aliyot in the parasha.

        :return: The metadata of the aliyot in the parasha.
        """
        return self._aliyot

    @property
    def chapter_verse_start(self) -> ChapterVerseMetadata:
        """
        Gets the starting chapter-verse pair of the parasha.

        :return: The starting chapter-verse pair of the parasha.
        """
        return self._chapter_verse_start

    @property
    def chapter_verse_end(self) -> ChapterVerseMetadata:
        """
        Gets the ending chapter-verse pair of the parasha.

        :return: The ending chapter-verse pair of the parasha.
        """
        return self._chapter_verse_end


class BookMetadata:
    """
    Metadata for a book. For each book, we have a list of parashiot (parasha metadata).
    """

    @staticmethod
    def _extract_metadata(book_name: str) -> List[ParashaMetadata]:
        """
        Get the metadata of the book.

        :param book_name: The name of the book whose metadata to extract.
        :return: The metadata of the book.
        """
        response = requests.get(f"{API_BASE_URL}/{book_name}", timeout=5)
        assert response.status_code == 200
        metadata = response.json()

        return [
            ParashaMetadata(name=parasha["sharedTitle"], aliya_metadata=parasha["refs"])
            for parasha in metadata["alt_structs"]["Parasha"]["nodes"]
        ]

    def __init__(self, book_name: str):
        self._name = book_name
        self._parshiot = BookMetadata._extract_metadata(book_name)

    @property
    def name(self) -> str:
        """
        Gets the name of the book.

        :return: The name of the book.
        """
        return self._name

    @property
    def parshiot(self) -> List[ParashaMetadata]:
        """
        Gets the metadate of the parashiot in the book.

        :return: The metadata of the parashiot in the book.
        """
        return self._parshiot
