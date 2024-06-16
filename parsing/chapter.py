from typing import List

from parsing.verse import Verse


class Chapter:
    """
    A Chapter is a sequence of verses.
    """

    def __init__(self, idx: int, verses: List[Verse]):
        self.idx = idx
        self._verses = verses

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

    def has_taam_sequence(
        self, taam_sequence: List[str], include_meshartim: bool = True
    ) -> bool:
        """
        Check if the Chapter contains a sequence of Taamim.

        :param taam_sequence: The sequence of Taamim.
        :return: True if the Verse contains the sequence, False otherwise.
        """
        for verse in self.verses:
            if verse.has_taam_sequence(taam_sequence, include_meshartim):
                return True
        return False

    def count_taam(self, taam_name: str) -> int:
        """
        Count the number of occurrences of a Taam in the Chapter.

        :param taam_name: The name of the Taam.
        :return: The number of occurrences of the Taam.
        """
        return sum(verse.count_taam(taam_name) for verse in self.verses)

    def __repr__(self) -> str:
        return "\n".join(
            [f"{self.idx}:{verse.idx} " + str(verse) for verse in self.verses]
        )
