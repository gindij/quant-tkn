from parsing import Book

BOOK_STRING = """‪xxxx    Unicode/XML Leningrad Codex [UXLC 2.0]‬
‪xxxx    Build: 27.1    -    19 Oct 2023  00:00‬
‪xxxx    Layout: Full; Content: Accents.‬
‪xxxx‬
‪xxxx    Genesis (50 chapters, 1533 verses).‬
‪xxxx‬
‪xxxx  Chapter 1   (31 verses)‬
‪xxxx‬
‫ 1  ׃1   בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃ ‬
‫ 2  ׃1   וְהָאָ֗רֶץ הָיְתָ֥ה תֹ֙הוּ֙ וָבֹ֔הוּ וְחֹ֖שֶׁךְ עַל־פְּנֵ֣י תְה֑וֹם וְר֣וּחַ אֱלֹהִ֔ים מְרַחֶ֖פֶת עַל־פְּנֵ֥י הַמָּֽיִם׃ ‬
‫ 3  ׃1   וַיֹּ֥אמֶר אֱלֹהִ֖ים יְהִ֣י א֑וֹר וַֽיְהִי־אֽוֹר׃ ‬
‫ 4  ׃1   וַיַּ֧רְא אֱלֹהִ֛ים אֶת־הָא֖וֹר כִּי־ט֑וֹב וַיַּבְדֵּ֣ל אֱלֹהִ֔ים בֵּ֥ין הָא֖וֹר וּבֵ֥ין הַחֹֽשֶׁךְ׃ ‬
‫ 5  ׃1   וַיִּקְרָ֨א אֱלֹהִ֤ים ׀ לָאוֹר֙ י֔וֹם וְלַחֹ֖שֶׁךְ קָ֣רָא לָ֑יְלָה וַֽיְהִי־עֶ֥רֶב וַֽיְהִי־בֹ֖קֶר י֥וֹם אֶחָֽד׃ פ ‬
‫ 6  ׃1   וַיֹּ֣אמֶר אֱלֹהִ֔ים יְהִ֥י רָקִ֖יעַ בְּת֣וֹךְ הַמָּ֑יִם וִיהִ֣י מַבְדִּ֔יל בֵּ֥ין מַ֖יִם לָמָֽיִם׃ ‬
‫ 7  ׃1   וַיַּ֣עַשׂ אֱלֹהִים֮ אֶת־הָרָקִיעַ֒ וַיַּבְדֵּ֗ל בֵּ֤ין הַמַּ֙יִם֙ אֲשֶׁר֙ מִתַּ֣חַת לָרָקִ֔יעַ וּבֵ֣ין הַמַּ֔יִם אֲשֶׁ֖ר מֵעַ֣ל לָרָקִ֑יעַ וֽ͏ַיְהִי־כֵֽן׃ ‬"""
BOOK_FILE_PATH = "data/cantillation/genesis.txt"


def test_book_from_string():
    book = Book.chapters_from_string(BOOK_STRING)
    assert book.name == "Genesis"
    assert len(book.chapters) == 1
    assert len(book.verses) == 7
    assert len(book.verses[0].taam_words) == 7


def test_book_from_text_file():
    book = Book.from_text_file(BOOK_FILE_PATH)
    assert book.name == "Genesis"
    assert len(book.chapters) == 50
    assert len(book.verses) == 1533
    assert len(book.verses[0].taam_words) == 7


def test_find_verses_with_taam_sequence():
    book = Book.chapters_from_string(BOOK_STRING)

    seq1 = ["maarikh", "tarha"]
    verses_with_meshartim = book.find_verses_with_taam_sequence(
        seq1, include_meshartim=True
    )
    num_verses_with_meshartim = len(
        [v for v in verses_with_meshartim["Bereshit"][0] if v[1].word_idxs != []]
    )
    assert num_verses_with_meshartim == 5, verses_with_meshartim

    verses_without_meshartim = book.find_verses_with_taam_sequence(
        seq1, include_meshartim=False
    )
    num_verses_without_meshartim = len(verses_without_meshartim["Bereshit"][0])
    # this should be 7 since the maarikh will be excluded so we will return the verses
    # that only have tarhas (which is all of them)
    assert num_verses_without_meshartim == 7

    seq2 = ["paseq", "pashta"]
    verses = book.find_verses_with_taam_sequence(seq2, include_meshartim=True)
    num_verses = len([v for v in verses["Bereshit"][0] if v[1] != []])
    assert num_verses == 1
