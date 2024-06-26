from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

from parsing.symbols import TAAM_ENGLISH_TO_HEBREW_NAMES

MIN_OCCURRENCES = 5


def plot_taamim_frequency_bar_chart(counts: Counter):
    """
    Plot a bar chart showing the frequency of each ta'am using plotly.

    :param counts: The frequency of each ta'am in a Counter object.
    """
    df = pd.DataFrame(counts.items(), columns=["Taam", "Count"]).sort_values(
        "Count", ascending=False
    )
    df.loc[:, "Taam Name"] = df["Taam"].apply(lambda n: TAAM_ENGLISH_TO_HEBREW_NAMES[n])
    fig = px.bar(df, x="Taam Name", y="Count")
    st.plotly_chart(fig)


def plot_taamim_sequence_frequency_bar_chart(
    counts: Counter, least_common: bool, top_k: int
):
    """
    Plot a bar chart showing the frequency of each ta'am sequence using plotly.

    :param counts: The frequency of each ta'am sequence in a Counter object.
    :param least_common: Whether to display the least common or most common ta'am sequences.
    :param top_k: The number of most/leaset common ta'am sequences to display.
    """
    df = pd.DataFrame(counts.items(), columns=["Taam Sequence", "Count"]).sort_values(
        "Count", ascending=least_common
    )
    df.loc[:, "Taam Sequence"] = df["Taam Sequence"].apply(
        # arrow pointing left
        lambda seq: "\u27F5".join([TAAM_ENGLISH_TO_HEBREW_NAMES[n] for n in seq])
    )
    df = df[df["Count"] >= MIN_OCCURRENCES]
    fig = px.bar(df.iloc[:top_k], x="Taam Sequence", y="Count")
    st.plotly_chart(fig)
