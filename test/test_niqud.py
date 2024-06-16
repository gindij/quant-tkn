import pytest

from parsing import Niqud


def test_niqud_from_name():
    niqud = Niqud.from_name("qamats")
    assert niqud.name == "qamats"
    assert niqud.symbol == "\u05B8"


def test_niqud_from_symbol():
    niqud = Niqud.from_symbol("\u05B8")
    assert niqud.name == "qamats"
    assert niqud.symbol == "\u05B8"


def test_niqud_from_name_invalid():
    with pytest.raises(AssertionError) as exc_info:
        Niqud.from_name("invalid")
    assert str(exc_info.value) == "Invalid niqud name: invalid"


def test_niqud_from_symbol_invalid():
    with pytest.raises(AssertionError) as exc_info:
        Niqud.from_symbol("invalid")
    assert str(exc_info.value) == "Invalid niqud symbol: invalid"


def test_niqud_equality():
    q1 = Niqud.from_name("qamats")
    q2 = Niqud.from_name("qamats")
    p = Niqud.from_name("patah")

    assert q1 == q2
    assert q1 != p
