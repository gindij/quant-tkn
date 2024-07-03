import pandas as pd
import streamlit as st

from parsing.symbols import (TAAM_HEBREW_TO_ENGLISH_NAMES,
                             convert_taam_name_to_symbol)
from streamlit_widgets import (double_taam_finder_widget,
                               overall_taam_distribution_widget,
                               taam_sequence_distribution_widget,
                               taam_sequence_finder_widget)

if __name__ == "__main__":
    st.title("Quantitative Ta'amim Analysis")
    st.write(
        "This app allows you to perform different quantitative analyses on the cantillation marks in the Bible."
    )

    about, taamim = st.tabs(["About", "Ta'amim"])

    with about:
        st.title("About")
        st.header("Why we built this...")
        st.write(
            """
            The ta'amim, or cantillation marks, are a set of symbols used in the Hebrew Bible to indicate the
            melodic chanting of the text, and also to instruct the reader about correct pronunciation and rhythm.
            Often, when preparing to read a particular Torah portion, I find myself thinking about basic statistical
            questions that it would be difficult to answer manually, such as how often certain combinations of ta'amim
            appear together, or how often a particular ta'am appears in a given book. This app aims to provide a simple,
            one-stop solution for answering these types of questions. The hope is that over time, we can build up an
            interesting collection of quantitative analyses of the ta'amim, and perhaps even discover some new insights
            into the structure of the Hebrew Bible.
            """
        )
        st.header("Ta'amim Guide")
        st.write(
            """
            The following table provides a guide to the different ta'amim symbols used in this app, along with their
            corresponding Hebrew and English names. Note that the names are those used in the Sephardic tradition.
            """
        )
        rows = []
        for hebrew_name, english_name in TAAM_HEBREW_TO_ENGLISH_NAMES.items():
            rows.append(
                (
                    hebrew_name,
                    english_name.replace("_", " "),
                    "ב" + convert_taam_name_to_symbol(english_name),
                )
            )
        guide = pd.DataFrame(rows, columns=["Hebrew Name", "English Name", "Symbol"])
        st.markdown(guide.style.hide(axis="index").to_html(), unsafe_allow_html=True)

        st.header("Sources")
        st.markdown(
            """
            The texts that underlie this app come from the [Leningrad Codex](http://tanach.us).
            The data about where aliyot start and end comes from [Sefaria](https://www.sefaria.org).
            """
        )

    with taamim:
        include_meshartim = st.checkbox("Include Meshartim", value=True)
        taam_sequence_finder_widget(include_meshartim=include_meshartim)
        double_taam_finder_widget(include_meshartim=include_meshartim)
        taam_sequence_distribution_widget(include_meshartim=include_meshartim)
        overall_taam_distribution_widget(include_meshartim=include_meshartim)
