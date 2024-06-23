import pytest

from parsing.metadata import *


def test_chapter_verse_metadata():
    metadata = ChapterVerseMetadata("1:2")
    assert metadata.chapter_idx == 1
    assert metadata.verse_idx == 2


def test_aliyah_metadata():
    metadata = AliyahMetadata(1, "Genesis 1:1-2:3")
    assert metadata.idx == 1
    assert metadata.start_chapter_verse.chapter_idx == 1
    assert metadata.start_chapter_verse.verse_idx == 1
    assert metadata.end_chapter_verse.chapter_idx == 2
    assert metadata.end_chapter_verse.verse_idx == 3


def test_book_metadata():
    metadata = BookMetadata("genesis")
    parshiot = metadata.parshiot

    assert len(parshiot) == 12
    assert all(len(p.aliyah_metadata) == 7 for p in parshiot)

    lechlecha = parshiot[2]
    assert lechlecha.name == "Lech Lecha"
    first_aliyah = lechlecha.aliyah_metadata[0]
    assert first_aliyah.idx == 0
    assert first_aliyah.start_chapter_verse.chapter_idx == 12
    assert first_aliyah.start_chapter_verse.verse_idx == 1
    assert first_aliyah.end_chapter_verse.chapter_idx == 12
    assert first_aliyah.end_chapter_verse.verse_idx == 13
