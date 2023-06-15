import streamlit as st
import time
import numpy as np
from utils import add_logo


add_logo()

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)
