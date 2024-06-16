from parsing.symbols import TAAMIM_SYMBOLS_TO_NAMES, TAAMIM_NAMES_TO_SYMBOLS


class Taam:
    """
    A Taam is a cantillation symbol in the Hebrew Bible.
    """

    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

    @classmethod
    def from_symbol(cls, symbol: str) -> "Taam":
        """
        Create a Taam object from a symbol.

        :param symbol: The symbol of the Taam.
        :return: A Taam object.
        """
        assert symbol in TAAMIM_SYMBOLS_TO_NAMES, f"Invalid taam symbol: {symbol}"
        return cls(TAAMIM_SYMBOLS_TO_NAMES[symbol], symbol)

    @classmethod
    def from_name(cls, name: str) -> "Taam":
        """
        Create a Taam object from a name.

        :param name: The name of the Taam.
        :return: A Taam object.
        """
        assert name in TAAMIM_NAMES_TO_SYMBOLS, f"Invalid taam name: {name}"
        return cls(name, TAAMIM_NAMES_TO_SYMBOLS[name])

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol and self.name == other.name
