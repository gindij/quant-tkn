from collections import Counter, defaultdict

import streamlit as st
import pandas as pd

from parsing import Book, TAAMIM
from plotting_utils import (
    plot_taamim_frequency_bar_chart,
    plot_taamim_sequence_frequency_bar_chart,
    MIN_OCCURRENCES,
)

ALL_BOOKS = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
ALL_TAAMIM = TAAMIM.values()


@st.cache_data
def load_all_books():
    """
    Load all books of the Bible.

    :return: A dictionary mapping book names to Book objects.
    """
    books = {}
    for book_name in ALL_BOOKS:
        book = Book.from_text_file(f"data/cantillation/{book_name}.txt")
        books[book_name] = book
    return books


@st.cache_data
def load_taamim_data(book_name: str) -> pd.DataFrame:
    """
    Load the taamim data for a given book.

    :param book_name: The name of the book whose taamim data should be loaded.
    :return: A Counter object containing the frequency of each ta'am in the book.
    """
    all_books = load_all_books()
    book = all_books[book_name]
    taamim = [taam.name for taam in book.taamim]
    taamim_counter = Counter(taamim)
    return taamim_counter


def render_taamim_analysis():
    """
    Render the high-level ta'amim analysis widget.
    """
    st.header("Ta'amim Frequency Analysis")
    st.write("This tool allows you to analyze the frequency of ta'amim in the Bible.")

    book_names = st.multiselect("Select a book", ALL_BOOKS)

    # create a bar chart showing the frequency of each ta'am in descending order
    # of frequency
    if len(book_names) > 0:
        total = Counter()
        for book_name in book_names:
            counts = load_taamim_data(book_name)
            total += counts

        plot_taamim_frequency_bar_chart(total)

    st.header("Most Common Ta'am Sequences")
    st.write(
        "This tool allows you to find the most common sequences of ta'amim in the Bible by sequence length."
    )

    seq_length = st.number_input("Sequence length", min_value=2, max_value=8)
    top_k = st.number_input("Number of combinations to show", min_value=5, max_value=50)
    most_or_least_common = st.radio("Most or least common", ["Most", "Least"])

    all_books = load_all_books()
    total = Counter()
    for book_name, book in all_books.items():
        taam_sequences = book.count_n_taam_sequences(seq_length)
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


def render_taamim_combination_finder():
    """
    Render the ta'amim combination finder widget.
    """
    st.header("Ta'amim Combination Finder")
    st.write(
        "This tool allows you to find all verses that contain a specific combination of ta'amim."
    )

    taam_sequence = st.multiselect("Select ta'amim", ALL_TAAMIM)

    all_books = load_all_books()

    if len(taam_sequence) > 0:
        verses = defaultdict(list)
        for book_name, book in all_books.items():
            verses[book_name].extend(book.find_verses_with_taam_sequence(taam_sequence))

        if sum(len(v) for v in verses.values()) == 0:
            st.write("No verses found with the selected ta'amim sequence.")
            return

        for book_name, verses in verses.items():
            if len(verses) == 0:
                continue
            with st.expander(f"{book_name}: {len(verses)} verses"):
                for verse in verses:
                    st.write(verse)


if __name__ == "__main__":
    render_taamim_analysis()
    render_taamim_combination_finder()
