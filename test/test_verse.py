from parsing import Verse


def test_verse_from_string():
    verse = Verse.from_string(0, "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃")
    taam_names = [taam.name for taam in verse.taamim]
    assert taam_names == [
        "tarha",
        "shofar_holekh",
        "atnah",
        "maarikh",
        "tarha",
        "maarikh",
        "maamid",
        "sof_passuq",
    ]
    taam_names_without_meshartim = [
        taam.name for taam in verse.taamim_without_meshartim
    ]
    assert taam_names_without_meshartim == [
        "tarha",
        "atnah",
        "tarha",
        "sof_passuq",
    ]


def test_verse_from_string_with_paseq():
    verse = Verse.from_string(
        0, "וַיִּקְרָ֨א אֱלֹהִ֤ים ׀ לָאוֹר֙ י֔וֹם וְלַחֹ֖שֶׁךְ קָ֣רָא לָ֑יְלָה וַֽיְהִי־עֶ֥רֶב וַֽיְהִי־בֹ֖קֶר י֥וֹם אֶחָֽד׃"
    )
    assert verse.has_taam("paseq")


def test_has_taam():
    verse = Verse.from_string(0, "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃")
    assert verse.has_taam("tarha")
    assert not verse.has_taam("zakef_katon")


def test_has_taam_qadma():
    verse = Verse.from_string(
        0, "וַיִּקְרָ֨א אֱלֹהִ֤ים׀ לָאוֹר֙ י֔וֹם וְלַחֹ֖שֶׁךְ קָ֣רָא לָ֑יְלָה וַֽיְהִי־עֶ֥רֶב וַֽיְהִי־בֹ֖קֶר י֥וֹם אֶחָֽד׃"
    )
    assert verse.has_taam("qadma")


def test_has_taam_azla_gerish():
    verse = Verse.from_string(
        0, "וַיֹּ֣אמֶר אֱלֹהִ֗ים יִקָּו֨וּ הַמַּ֜יִם מִתַּ֤חַת הַשָּׁמַ֙יִם֙ אֶל־מָק֣וֹם אֶחָ֔ד וְתֵרָאֶ֖ה הַיַּבָּשָׁ֑ה וַֽיְהִי־כֵֽן׃"
    )
    assert verse.has_taam("azla")
    assert verse.has_taam("gerish")


def test_find_taam_sequence():
    verse = Verse.from_string(0, "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃")
    assert verse.find_taam_sequence(
        ["tarha", "atnah", "tarha"], include_meshartim=False
    ).word_idxs == [[0, 2, 4]]
    assert verse.find_taam_sequence(["tarha"], include_meshartim=False).word_idxs == [
        [0],
        [4],
    ]
    assert (
        verse.find_taam_sequence(["tarha", "atnah", "tarha"], include_meshartim=True)
        is None
    )


def test_count_taam():
    verse = Verse.from_string(0, "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃")
    assert verse.count_taam("tarha") == 2
    assert verse.count_taam("zakef_katon") == 0
