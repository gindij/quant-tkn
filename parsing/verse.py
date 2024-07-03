from typing import List, Optional

from parsing.symbols import TAAME_MESHARET
from parsing.taam import Taam
from parsing.word import Word


class TaamSequenceResult:
    """
    A TaamSequenceResult is a result of a search for a sequence of Taamim.
    """

    def __init__(self, word_idxs: List[List[int]]):
        self._word_idxs = word_idxs

    @property
    def word_idxs(self) -> List[List[int]]:
        """
        Get the indices of the words in the Taam sequence.

        :return: The indices of the words in the Taam sequence.
        """
        return self._word_idxs

    def __iter__(self):
        return iter(self._word_idxs)


class Verse:
    """
    A Verse is a sequence of words.
    """

    def __init__(self, idx: int, words: List[Word]):
        self.idx = idx
        self._words = words
        self._letters = [letter for word in words for letter in word.letters]
        self._taamim = [taam for word in words for taam in word.taamim]
        self._taamim_without_meshartim = [
            taam for word in words for taam in word.taamim_without_meshartim
        ]
        self._nequdot = [niqud for letter in self._letters for niqud in letter.nequdot]

    @staticmethod
    def trim_word_list(words: List[Word]) -> List[Word]:
        """
        Remove empty words from the list of words.

        :param words: The list of words.
        :return: The list of words with empty words removed.
        """
        while len(words[-1]) == 0:
            words.pop()
        while len(words[0]) == 0:
            words.pop(0)
        return words

    @classmethod
    def from_string(cls, idx: int, s: str) -> "Verse":
        """
        Parse a pasuk from a string.

        :param idx: The index of the Verse (within a Chapter).
        :param s: The string representation of the Verse.
        :return: A Verse object.
        """
        words = []
        for w in s.split():
            if w == "\u05C0":
                new_letters = words[-1].letters
                new_letters[-1].add_taam(Taam.from_name("paseq"))
                # trigger re-eval of constructor to make sure paseq is included
                words[-1] = Word(new_letters)
                continue
            words.append(Word.from_string(w))

        # change any qadmas that are followed by a gerish to azlas
        for wd1, wd2 in zip(words, words[1:]):
            if wd1.has_taam("qadma") and (
                wd2.has_taam("gerish") or wd1.has_taam("gerish")
            ):
                wd1.rename_taam("qadma", "azla")

        return cls(idx, Verse.trim_word_list(words))

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
    def taamim_without_meshartim(self):
        """
        Get the taamim in the Verse without the meshartim.

        :return: The taamim in the Verse without the meshartim.
        """
        return self._taamim_without_meshartim

    @property
    def nequdot(self):
        """
        Get the nequdot in the Verse.

        :return: The nequdot in the Verse.
        """
        return self._nequdot

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

    def find_taam_sequence(
        self, taam_sequence: List[str], include_meshartim: bool = True
    ) -> Optional[TaamSequenceResult]:
        """
        Check if the Verse contains a sequence of Taamim.

        :param taam_sequence: The sequence of Taamim.
        :return: The inner lists are the indices of the words in a sequence.
                 If there is more than one sequence, the outer list contains
                 all the sequences.
        """
        # exclude meshartim if necessary
        if not include_meshartim:
            taam_sequence = [
                taam_name
                for taam_name in taam_sequence
                if taam_name not in TAAME_MESHARET
            ]
        seqs = []
        curr_seq, seq_idx = [], 0
        for word_idx, word in enumerate(self._words):
            for letter in word:

                if seq_idx == len(taam_sequence):
                    seqs.append(curr_seq)
                    curr_seq, seq_idx = [], 0
                    break

                if len(letter.taamim) == 0 or (
                    not include_meshartim
                    and any(t.name in TAAME_MESHARET for t in letter.taamim)
                ):
                    continue

                if letter.has_taam(taam_sequence[seq_idx]):
                    curr_seq.append(word_idx)
                    seq_idx += 1
                else:
                    curr_seq, seq_idx = [], 0

        if seq_idx == len(taam_sequence):
            seqs.append(curr_seq)
        seqs = [sorted(set(seq)) for seq in seqs]
        return TaamSequenceResult(seqs)

    def count_taam(self, taam_name: str) -> int:
        """
        Count the number of occurrences of a Taam in the Verse.

        :param taam_name: The name of the Taam.
        :return: The number of occurrences of the Taam.
        """
        return sum(word.has_taam(taam_name) for word in self._words)

    def __iter__(self):
        return iter(self._words)

    def __repr__(self) -> str:
        return " ".join([str(word) for word in self._words])
