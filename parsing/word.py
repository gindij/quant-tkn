from typing import List

from parsing.letter import Letter
from parsing.symbols import TAAME_MESHARET, LETTERS
from parsing.taam import Taam


class Word:
    """
    A Word is a sequence of letters.
    """

    def _get_clean_taamim(self):
        """
        Get the taamim in the Word.

        :return: The taamim in the Word.
        """
        taamim = self._taamim_raw

        if len(taamim) == 2 and all(taam.name == "pashta" for taam in taamim):
            return [Taam.from_name("tere_qadmin")]

        if (
            len(taamim) == 1
            and taamim[0].name == "pashta"
            and not self.letters[-1].has_taam("pashta")
        ):
            return [Taam.from_name("qadma")]

        return taamim

    def __init__(self, letters: List[Letter]):
        self._letters = letters
        self._taamim_raw = [taam for letter in self._letters for taam in letter.taamim]
        self._taamim_clean = self._get_clean_taamim()
        self._nequdot = [niqud for letter in self._letters for niqud in letter.nequdot]

    @classmethod
    def from_string(cls, word: str) -> "Word":
        """
        Create a Word from a string.

        :param word: The string to create the Word from.
        :return: The Word.
        """
        letters = []
        for i, letter in enumerate(word):
            if letter in LETTERS:
                curr_letter = [letter]
                for j in range(i + 1, len(word)):
                    if word[j] in LETTERS:
                        break
                    curr_letter.append(word[j])
                letters.append(Letter.from_string("".join(curr_letter)))
        return cls(letters)

    @property
    def taamim_without_meshartim(self):
        """
        Get the taamim in the Word without the meshartim.

        :return: The taamim in the Word without the meshartim.
        """
        return [taam for taam in self._taamim_clean if taam.name not in TAAME_MESHARET]

    @property
    def taamim_raw(self):
        """
        Get the raw taamim in the Word.

        :return: The raw taamim in the Word.
        """
        return self._taamim_raw

    @property
    def taamim(self):
        """
        Get the taamim in the Word.

        :return: The taamim in the Word.
        """
        return self._taamim_clean

    @property
    def letters(self):
        """
        Get the letters in the Word.

        :return: The letters in the Word.
        """
        return self._letters

    @property
    def nequdot(self):
        """
        Get the nequdot in the Word.

        :return: The nequdot in the Word.
        """
        return self._nequdot

    def has_taam(self, taam_name: str) -> bool:
        """
        Check if the Word contains a Taam.

        :param taam_name: The name of the Taam.
        :return: True if the Word contains the Taam, False otherwise.
        """
        return any(taam.name == taam_name for taam in self._taamim_clean)

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

    def __repr__(self) -> str:
        return "".join([str(letter) for letter in self.letters])

    def __len__(self) -> int:
        return len(self.letters)
