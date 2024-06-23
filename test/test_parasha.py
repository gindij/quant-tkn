from parsing.book import Book


def test_parasha_extraction():
    book = Book.from_text_file("data/cantillation/genesis.txt")

    assert book.name == "Genesis"
    assert len(book.parshiot) == 12

    bereshit = book.parshiot[0]
    assert bereshit.name == "Bereshit"
    assert len(bereshit.aliyot) == 7
    assert len(bereshit.aliyot[0]) == 34
    assert len(bereshit.aliyot[1]) == 16
    assert len(bereshit.aliyot[2]) == 27
    assert len(bereshit.aliyot[3]) == 21
    assert len(bereshit.aliyot[4]) == 4
    assert len(bereshit.aliyot[5]) == 28
    assert len(bereshit.aliyot[6]) == 16

    assert len(bereshit) == 146
