import pytest

from parsing import Letter, Niqud, Taam


def test_letter_from_string():
    letter = Letter.from_string("שִׁ֖")
    assert letter.letter == "ש"
    assert letter.taamim == [Taam.from_name("tarha")]
    assert letter.nequdot == [Niqud.from_name("shin_dot"), Niqud.from_name("hiriq")]


def test_letter_only():
    letter = Letter("א")
    assert letter.letter == "א"
    assert letter.taamim == []
    assert letter.nequdot == []


def test_letter_with_taam():
    pazer = Taam.from_name("pazer_gadol")
    letter = Letter("א", taamim=[pazer])
    assert letter.letter == "א"
    assert letter.taamim == [pazer]
    assert letter.nequdot == []


def test_letter_with_taam_and_niqud():
    pazer = Taam.from_name("pazer_gadol")
    qamats = Niqud.from_name("qamats")
    letter = Letter("א", taamim=[pazer], nequdot=[qamats])
    assert letter.letter == "א"
    assert letter.taamim == [pazer]
    assert letter.nequdot == [qamats]


def test_letter_add_taam():
    letter = Letter("א")
    assert letter.letter == "א"
    assert letter.taamim == []

    pazer = Taam.from_name("pazer_gadol")
    letter.add_taam(pazer)
    assert letter.letter == "א"
    assert letter.taamim == [pazer]


def test_letter_has_taam():
    pazer = Taam.from_name("pazer_gadol")
    letter = Letter("א", taamim=[pazer])
    assert letter.has_taam("pazer_gadol")
    assert not letter.has_taam("pazer_katan")
    assert not letter.has_taam("zaqef_gadol")


def test_rename_taam():
    pazer = Taam.from_name("pazer_gadol")
    letter = Letter("א", taamim=[pazer])
    assert letter.has_taam("pazer_gadol")

    letter.rename_taam("pazer_gadol", "pazer_katan")
    assert not letter.has_taam("pazer_gadol")
    assert letter.has_taam("pazer_katan")


def test_is_maqaf():
    letter = Letter("־")
    assert letter.is_maqaf

    letter = Letter("מ")
    assert not letter.is_maqaf
