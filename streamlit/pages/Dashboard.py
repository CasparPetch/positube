import pandas as pd
import streamlit as st
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
# from scripts.channel_search import grab_channel
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import os
import random

st.set_page_config(page_title="Dashboard", page_icon="📈")

st.markdown("# Dashboard")
st.sidebar.header("Dashboard")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

st.text("")
st.text("")

# Enter channel ID

channel_id = st.text_input("Enter Channel ID")
# comments_df = grab_channel(channel_id)
if channel_id is not None:
    if st.button("Tube me"):
        st.write("### Bar chart")
        st.write("### Visualization")

# Line breaks

st.text("")
st.text("")

# Basic Statistics

st.caption(f"Pewdiepie has 50 million views")
st.caption('Pewdiepie has 400,340 subscribers')
st.caption('Pewdiepie has 135 videos')
st.caption('Pewdiepie is generally positive amongst viewers')

# Charts and Bars
# 1
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Video", "Views", "ID"])

st.bar_chart(chart_data)

# 2
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)

# 3
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.area_chart(chart_data)
