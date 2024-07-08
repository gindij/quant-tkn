from typing import Counter, Iterator, List, Tuple

from parsing.verse import VerseTaamSequenceResult, Verse


class AliyahTaamSequenceResult:
    """
    An AliyahTaamSequenceResult is a result of a search for a sequence of Taamim
    for all verses in an Aliyah.
    """

    def __init__(self, verse_results: List[VerseTaamSequenceResult]):
        self._verse_results = verse_results

    @property
    def verse_results(self) -> VerseTaamSequenceResult:
        """
        A collection of verse results across an Aliyah.

        :return: The verse results.
        """
        return self._verse_results

    def __iter__(self) -> Iterator[Tuple[Verse, VerseTaamSequenceResult]]:
        return iter(self._verse_results)


class Aliyah:
    """
    An Aliyah is a collection of verses possibly spanning more than
    one chapter.
    """

    def __init__(self, idx: int, verses: List[Verse]):
        self._idx = idx
        self._verses = verses

    @property
    def idx(self) -> int:
        """
        Gets the index of the aliyah (0 - 6 inclusive).

        :return: The index of the aliyah.
        """
        return self._idx

    @property
    def verses(self) -> List[Verse]:
        """
        Gets the verses in the aliyah.

        :return: The verses in the aliyah.
        """
        return self._verses

    def find_verses_with_taam_sequence(
        self, taam_sequence: List[str], include_meshartim: bool = True
    ) -> AliyahTaamSequenceResult:
        """
        Find verses with a sequence of Taamim.

        :param taam_sequence: The sequence of Taamim.
        :param include_meshartim: Whether to include Meshartim in the search.
        :return: The verses with the Taam sequence.
        """
        results = []
        for verse in self.verses:
            result = verse.find_taam_sequence(taam_sequence, include_meshartim)
            if result.word_idxs:
                results.append((verse, result))
        return results

    def count_n_taam_sequences(self, n: int, include_meshartim: bool = True) -> Counter:
        """
        Count the number of n-Taam sequences in the Aliyah.

        :param n: The length of the Taam sequence.
        :param include_meshartim: Whether to include Meshartim in the search.
        :return: A Counter mapping taam sequences to their counts.
        """
        taam_sequence_counts = Counter()
        for verse in self.verses:
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

    def __len__(self) -> int:
        return len(self._verses)

    def __iter__(self) -> Iterator[Verse]:
        return iter(self._verses)
