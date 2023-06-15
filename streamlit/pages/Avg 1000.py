import streamlit as st
import time
import numpy as np
from utils import add_logo


add_logo()

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Avg 1000")
st.sidebar.header("Avg 1000")
st.write(
    """This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)
