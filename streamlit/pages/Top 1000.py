import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

st.markdown("# DataFrame top 1000")
st.sidebar.header("DataFrame top 1000")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)
