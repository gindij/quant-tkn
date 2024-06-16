import pytest

from parsing import Taam, Word


def test_word_with_one_taam():
    word = Word.from_string("בְּרֵאשִׁ֖ית")
    assert word.taamim_without_meshartim == [Taam.from_name("tarha")]
    assert word.taamim == [Taam.from_name("tarha")]


def test_word_with_tere_kadmin():
    word = Word.from_string("תֹ֙הוּ֙")
    assert word.taamim_raw == [Taam.from_name("pashta"), Taam.from_name("pashta")]
    assert word.taamim == [Taam.from_name("tere_qadmin")]
    assert word.taamim_without_meshartim == [Taam.from_name("tere_qadmin")]

    assert word.has_taam("tere_qadmin")
    assert not word.has_taam("pashta")


def test_meshartim():
    word = Word.from_string("וַיֹּ֣אמֶר")
    assert word.taamim_raw == [Taam.from_name("shofar_holekh")]
    assert word.taamim == [Taam.from_name("shofar_holekh")]
    assert word.taamim_without_meshartim == []


def test_rename_taam():
    word = Word.from_string("לָאוֹר֙")
    assert word.has_taam("pashta")
    assert len(word.taamim_without_meshartim) == 1

    assert word.rename_taam("pashta", "qadma")
    assert not word.has_taam("pashta")
    assert word.has_taam("qadma")

    assert len(word.taamim_without_meshartim) == 0
