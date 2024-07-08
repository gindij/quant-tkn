from typing import List, Optional

from parsing.niqud import Niqud
from parsing.symbols import MAQAF, NEQUDOT_SYMBOLS, TAAMIM_SYMBOLS
from parsing.taam import Taam


class Letter:
    """
    A Letter is a character in the Hebrew alphabet with a Taam and possibly a Dagesh.
    """

    def __init__(
        self,
        letter: str,
        taamim: Optional[List[Taam]] = None,
        nequdot: Optional[List[Niqud]] = None,
    ):
        if nequdot is None:
            nequdot = []

        if taamim is None:
            taamim = []

        self._letter = letter
        self._taamim = taamim
        self._nequdot = nequdot

    @classmethod
    def from_string(cls, full_letter: str) -> "Letter":
        """
        Create a Letter from a string.

        :param full_letter: The string to create the Letter from. Includes nequdot and taamim.
        :return: The Letter.
        """
        letter = full_letter[0]
        nequdot, taamim = [], []
        for i in range(1, len(full_letter)):
            ci = full_letter[i]
            if ci in TAAMIM_SYMBOLS:
                taamim.append(Taam.from_symbol(ci))
            elif ci in NEQUDOT_SYMBOLS:
                nequdot.append(Niqud.from_symbol(ci))
        return cls(letter, taamim, nequdot)

    @property
    def is_maqaf(self):
        """
        Check if the Letter is a maqaf.

        :return: True if the Letter is a maqaf, False otherwise.
        """
        return self.letter == MAQAF

    @property
    def taamim(self):
        """
        Get the Taamim in the Letter.

        :return: The Taamim in the Letter.
        """
        return self._taamim

    @property
    def nequdot(self):
        """
        Get the niqud in the Letter.

        :return: The niqud in the Letter.
        """
        return self._nequdot

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

    def add_niqud(self, niqud: Niqud):
        """
        Add a vowel (niqud) to the Letter.

        :param niqud: The niqud to add.
        """
        self._nequdot.append(niqud)

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
        nequdot = "".join([niqud.symbol for niqud in self.nequdot])
        return f"{self.letter}{nequdot}{taamim}"
