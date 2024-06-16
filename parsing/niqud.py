from parsing.symbols import (NEQUDOT_NAMES, NEQUDOT_NAMES_TO_SYMBOLS,
                             NEQUDOT_SYMBOLS, NEQUDOT_SYMBOLS_TO_NAMES)


class Niqud:
    """
    A niqud is a vowel symbol in the Hebrew Bible.
    """

    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

    @classmethod
    def from_symbol(cls, symbol: str) -> "Niqud":
        """
        Create a Niqud object from its symbol.

        :param symbol: The symbol of the Niqud.
        :return: A Niqud object.
        """
        assert symbol in NEQUDOT_SYMBOLS, f"Invalid niqud symbol: {symbol}"
        return cls(NEQUDOT_SYMBOLS_TO_NAMES[symbol], symbol)

    @classmethod
    def from_name(cls, name: str) -> "Niqud":
        """
        Create a Niqud object from its name.

        :param name: The name of the Niqud.
        :return: A Niqud object.
        """
        assert name in NEQUDOT_NAMES_TO_SYMBOLS, f"Invalid niqud name: {name}"
        return cls(name, NEQUDOT_NAMES_TO_SYMBOLS[name])

    def __repr__(self):
        return self.symbol

    def __eq__(self, value: object) -> bool:
        return self.name == value.name and self.symbol == value.symbol
