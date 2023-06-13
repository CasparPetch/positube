import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="About us", page_icon="🌍")

st.markdown("# About us")
st.sidebar.header("About us")
st.write(
    """This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)
