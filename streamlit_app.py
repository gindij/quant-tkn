import streamlit as st

from streamlit_widgets import (
    taam_distribution_widget,
    taam_sequence_distribution_widget,
    taam_sequence_finder_widget,
)

if __name__ == "__main__":
    st.title("Quantitative Ta'amim Analysis")
    st.write(
        "This app allows you to perform different quantitative analyses on the cantillation marks in the Bible."
    )
    include_meshartim = st.checkbox("Include Meshartim", value=True)
    taam_distribution_widget(include_meshartim=include_meshartim)
    taam_sequence_distribution_widget(include_meshartim=include_meshartim)
    taam_sequence_finder_widget(include_meshartim=include_meshartim)
