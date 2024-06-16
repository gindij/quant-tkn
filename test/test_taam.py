import pytest

from parsing import Taam


def test_taam_from_name():
    taam = Taam.from_name("zaqef_qaton")
    assert taam.name == "zaqef_qaton"
    assert taam.symbol == "\u0594"


def test_taam_from_symbol():
    taam = Taam.from_symbol("\u0594")
    assert taam.name == "zaqef_qaton"
    assert taam.symbol == "\u0594"


def test_taam_from_invalid_name():
    with pytest.raises(AssertionError) as exc_info:
        Taam.from_name("a")
    assert str(exc_info.value) == "Invalid taam name: a"


def test_taam_from_invalid_symbol():
    with pytest.raises(AssertionError) as exc_info:
        Taam.from_symbol("a")
    assert str(exc_info.value) == "Invalid taam symbol: a"


def test_taam_equality():
    zq1 = Taam.from_name("zaqef_qaton")
    zq2 = Taam.from_name("zaqef_qaton")
    zg = Taam.from_name("zaqef_gadol")

    assert zq1 == zq2
    assert zq1 != zg
