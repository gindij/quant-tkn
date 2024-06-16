from collections import Counter, defaultdict
import pandas as pd
import pathlib
import streamlit as st
from typing import Dict

from parsing.symbols import TAAMIM_NAMES
from parsing import Book
from utils.plotting_utils import (
    plot_taamim_frequency_bar_chart,
    plot_taamim_sequence_frequency_bar_chart,
    MIN_OCCURRENCES,
)

ALL_BOOK_NAMES = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
BASE_PATH = pathlib.Path(__file__).parent.resolve()


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
    taamim = [
        taam.name
        for taam in (
            book.taamim if include_meshartim else book.taamim_without_meshartim
        )
    ]
    taamim_counter = Counter(taamim)
    return taamim_counter


def taam_distribution_widget(include_meshartim: bool):
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


def taam_sequence_finder_widget(include_meshartim: bool):
    """
    Render the ta'amim sequence finder widget.

    :param include_meshartim: Whether to include meshartim in the analysis.
    """
    st.header("Ta'amim Sequence Finder")
    st.write(
        "This tool allows you to find all verses that contain a specific sequence of ta'amim."
    )

    taam_sequence = st.multiselect("Select ta'amim", sorted(TAAMIM_NAMES))

    if len(taam_sequence) > 0:
        verses = defaultdict(list)
        for book_name in ALL_BOOK_NAMES:
            book = load_book(book_name)
            verses[book_name].extend(
                book.find_verses_with_taam_sequence(taam_sequence, include_meshartim)
            )

        if sum(len(v) for v in verses.values()) == 0:
            st.write("No verses found with the selected ta'amim sequence.")
            return

        for book_name, verses in verses.items():
            if len(verses) == 0:
                continue
            with st.expander(f"{book_name}: {len(verses)} verses"):
                for verse in verses:
                    st.write(verse)
