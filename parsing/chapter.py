from typing import List

from parsing.verse import Verse


class Chapter:
    """
    A Chapter is a sequence of verses.
    """

    def __init__(self, idx: int, verses: List[Verse]):
        self._idx = idx
        self._verses = verses

    @property
    def verses(self):
        """
        Get the verses in the Chapter.

        :return: The verses in the Chapter.
        """
        return self._verses

    @property
    def idx(self):
        """
        Get the index of the Chapter.

        :return: The index of the Chapter.
        """
        return self._idx

    def add_verse(self, verse: Verse):
        """
        Add a verse to the Chapter.

        :param verse: The verse to add.
        """
        self._verses.append(verse)

    def __repr__(self) -> str:
        return "\n".join(
            [f"{self._idx}:{verse.idx} " + str(verse) for verse in self.verses]
        )
