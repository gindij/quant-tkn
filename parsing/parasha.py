from typing import Counter, List

from parsing.aliyah import Aliyah, AliyahTaamSequenceResult
from parsing.chapter import Chapter
from parsing.metadata import ParashaMetadata


class ParashaTaamSequenceResult:
    """
    A ParashaTaamSequenceResult is a result of a search for a sequence of Taamim
    for all verses in a Parasha.
    """

    def __init__(self, aliyah_results: List[AliyahTaamSequenceResult]) -> None:
        assert len(aliyah_results) == 7
        self._aliyah_results = aliyah_results

    @property
    def aliyah_results(self) -> List[AliyahTaamSequenceResult]:
        """
        Get the results of the search for Taamim in the Parasha.

        :return: The results of the search for Taamim in the Parasha.
        """
        return self._aliyah_results


class Parasha:
    """
    A Parasha is a collection of aliyot.
    """

    def __init__(self, name: str, aliyot: List[Aliyah]) -> None:
        self._name = name
        self._aliyot = aliyot

    @classmethod
    def from_chapters(
        cls, metadata: ParashaMetadata, chapters: List[Chapter]
    ) -> "Parasha":
        """
        Extract the Parasha from the sequence of chapters and the
        Parasha's metadata (with information about where aliyot start and end).

        :param metadata: Metadata of the parasha containing information about
                         where aliyot start and end.
        :param chapters: The sequence of chapters in a book.
        :return: The Parasha object.
        """
        aliyot = []
        for aliyah in metadata.aliyah_metadata:
            aliyah_start_chapter_idx = aliyah.start_chapter_verse.chapter_idx
            aliyah_end_chapter_idx = aliyah.end_chapter_verse.chapter_idx
            aliyah_start_verse_idx = aliyah.start_chapter_verse.verse_idx
            aliyah_end_verse_idx = aliyah.end_chapter_verse.verse_idx
            verses = []
            for chapter in chapters:
                if chapter.idx < aliyah_start_chapter_idx:
                    continue
                if chapter.idx > aliyah_end_chapter_idx:
                    break
                for verse in chapter.verses:
                    if (
                        chapter.idx == aliyah_start_chapter_idx
                        and verse.idx < aliyah_start_verse_idx
                    ):
                        continue
                    if (
                        chapter.idx == aliyah_end_chapter_idx
                        and verse.idx > aliyah_end_verse_idx
                    ):
                        break
                    verses.append(verse)
            aliyot.append(Aliyah(aliyah.idx, verses))
        return cls(metadata.name, aliyot)

    @property
    def name(self) -> str:
        """
        Get the name of the Parasha.

        :return: The name of the Parasha.
        """
        return self._name

    @property
    def aliyot(self) -> List[Aliyah]:
        """
        Get the aliyot in the Parasha.

        :return: The aliyot in the Parasha.
        """
        return self._aliyot

    def find_verses_with_taam_sequence(
        self, taam_sequence: List[str], include_meshartim: bool = True
    ) -> ParashaTaamSequenceResult:
        """
        Find the verses in the Parasha that contain a sequence of Taamim.

        :param taam_sequence: The sequence of Taamim.
        :param include_meshartim: Whether to include Meshartim in the search.
        :return: A dictionary mapping the index of the Aliyah to the list of
                 verses in the Aliyah that contain the sequence of Taamim.
        """
        verses_by_aliyah = []
        for aliyah in self.aliyot:
            aliyah_verse_match_pairs = aliyah.find_verses_with_taam_sequence(
                taam_sequence, include_meshartim
            )
            if aliyah_verse_match_pairs:
                verses_by_aliyah.append(aliyah_verse_match_pairs)
        return verses_by_aliyah

    def count_n_taam_sequences(self, n: int, include_meshartim: bool = True) -> Counter:
        """
        Count the number of n-Taam sequences in the Parasha.

        :param n: The number of Taamim in the sequence.
        :param include_meshartim: Whether to include Meshartim in the search.
        :return: A counter object with the n-Taam sequences and their counts.
        """
        totals = Counter()
        for aliyah in self.aliyot:
            totals += aliyah.count_n_taam_sequences(n, include_meshartim)
        return totals

    def __len__(self) -> int:
        return sum(len(aliyah) for aliyah in self.aliyot)
