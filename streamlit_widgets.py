import pathlib
from collections import Counter
from typing import List

import pandas as pd
import streamlit as st

from parsing import Book
from parsing.symbols import TAAM_HEBREW_TO_ENGLISH_NAMES, TAAME_MESHARET
from utils.plotting_utils import (
    MIN_OCCURRENCES,
    plot_taamim_frequency_bar_chart,
    plot_taamim_sequence_frequency_bar_chart,
)

ALL_BOOK_NAMES = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
BASE_PATH = pathlib.Path(__file__).parent.resolve()
HIGHLIGHT_COLOR = "#0362fc"


@st.cache_data
def load_book(book_name: str) -> Book:
    """
    Load all books of the Bible.

    :return: A dictionary mapping book names to Book objects.
    """
    return Book.from_text_file(
        BASE_PATH / "data" / "cantillation" / f"{book_name.lower()}.txt"
    )


def extract_taamim_data(book: Book, include_meshartim: bool = True) -> pd.DataFrame:
    """
    Load the taamim data for a given book.

    :param book: The Book object to analyze.
    :param include_meshartim: Whether to include meshartim in the analysis.
    :return: A Counter object containing the frequency of each ta'am in the book.
    """
    taamim = book.taamim if include_meshartim else book.taamim_without_meshartim
    taam_names = [t.name for t in taamim]
    return Counter(taam_names)


def overall_taam_distribution_widget(include_meshartim: bool):
    """
    Render the ta'amim distribution widget.

    :param include_meshartim: Whether to include meshartim in the analysis.
    """
    st.header("Ta'amim Frequency Analysis")
    st.write("This tool allows you to analyze the frequency of ta'amim in the Bible.")

    book_names = st.multiselect("Select a book", ALL_BOOK_NAMES)

    # create a bar chart showing the frequency of each ta'am in descending order
    # of frequency
    if len(book_names) > 0:
        total = Counter()
        for book_name in book_names:
            book = load_book(book_name)
            total += extract_taamim_data(book, include_meshartim)

        plot_taamim_frequency_bar_chart(total)


def taam_sequence_distribution_widget(include_meshartim: bool):
    """
    Render the high-level ta'amim analysis widget.

    :param include_meshartim: Whether to include meshartim in the analysis.
    """

    st.header("Most Common Ta'am Sequences")
    st.write(
        "This tool allows you to find the most common sequences of ta'amim in the Bible by sequence length."
    )

    seq_length = st.number_input("Sequence length", min_value=2, max_value=8)
    top_k = st.number_input("Number of combinations to show", min_value=5, max_value=50)
    most_or_least_common = st.radio("Most or least common", ["Most", "Least"])

    total = Counter()
    for book_name in ALL_BOOK_NAMES:
        book = load_book(book_name)
        taam_sequences = book.count_n_taam_sequences(seq_length, include_meshartim)
        if len(taam_sequences) == 0:
            continue
        total += Counter(taam_sequences)

    if len(total) == 0:
        st.write("No ta'am sequences found.")
        return

    st.write(
        f"{top_k} {most_or_least_common.lower()} common {seq_length}-ta'am sequences (≥ {MIN_OCCURRENCES} occurrences):"
    )
    plot_taamim_sequence_frequency_bar_chart(
        counts=total, top_k=top_k, least_common=most_or_least_common == "Least"
    )


def _highlight_word(word_str: str, color: str):
    return f'<span style="color:{color}">**{word_str}**</span>'


def _taam_seq_finder_widget(taam_sequence: List[str], include_meshartim: bool):
    if len(taam_sequence) > 0:
        book_dict = {
            book_name: load_book(book_name).find_verses_with_taam_sequence(
                [TAAM_HEBREW_TO_ENGLISH_NAMES[taam] for taam in taam_sequence],
                include_meshartim,
            )
            for book_name in ALL_BOOK_NAMES
        }
        if sum(len(v) for v in book_dict.values()) == 0:
            st.write("No verses found with the selected ta'amim sequence.")
            return

        for book_name, verse_dict in book_dict.items():
            with st.expander(book_name):
                for parasha_name, parasha_result in verse_dict.items():
                    if any(v for v in parasha_result):
                        st.markdown(f"### {parasha_name}")
                    for i, aliyah_result in enumerate(parasha_result):
                        if len(aliyah_result) > 0:
                            st.markdown(f"#### Aliyah {i + 1}")
                        for verse, verse_result in aliyah_result:
                            if len(verse_result.word_idxs) > 0:
                                flat_idxs = {
                                    idx
                                    for idx_list in verse_result.word_idxs
                                    for idx in idx_list
                                }
                                # display the part of the verse with the ta'am sequence in green
                                wds = [
                                    (
                                        _highlight_word(
                                            word_str=word, color=HIGHLIGHT_COLOR
                                        )
                                        if ix in flat_idxs
                                        else str(word)
                                    )
                                    for ix, word in enumerate(verse.taam_words)
                                ]
                                st.markdown(" ".join(wds), unsafe_allow_html=True)


def taam_sequence_finder_widget(include_meshartim: bool):
    """
    Render the ta'amim sequence finder widget.

    :param include_meshartim: Whether to include meshartim in the analysis.
    """
    st.header("Ta'amim Sequence Finder")
    st.write(
        "This tool allows you to find all verses that contain a specific sequence of ta'amim."
    )
    valid_taamim = sorted(TAAM_HEBREW_TO_ENGLISH_NAMES.keys())
    if not include_meshartim:
        valid_taamim = [taam for taam in valid_taamim if taam not in TAAME_MESHARET]
    taam_sequence = st.multiselect(
        "Select ta'amim", valid_taamim, placeholder="Choose one or more ta'amim"
    )
    _taam_seq_finder_widget(taam_sequence, include_meshartim)


def double_taam_finder_widget(include_meshartim: bool):
    """
    Render the double ta'amim finder widget.

    :param include_meshartim: Whether to include meshartim in the analysis.
    """
    st.header("Double Ta'amim Finder")
    st.write(
        "This tool allows you to find all verses that contain a particular ta'am twice in a row."
    )
    valid_taamim = sorted(TAAM_HEBREW_TO_ENGLISH_NAMES.keys())
    if not include_meshartim:
        valid_taamim = [taam for taam in valid_taamim if taam not in TAAME_MESHARET]
    taam = st.selectbox("Select ta'amim", valid_taamim)
    _taam_seq_finder_widget([taam, taam], include_meshartim)
