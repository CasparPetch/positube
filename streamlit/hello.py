import pandas as pd
import streamlit as st
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import os
import random
from st_clickable_images import clickable_images

st.set_page_config(
    page_title="Positube",
    page_icon="👋",
)

st.write("# Welcome to Positube! 👋")
st.sidebar.success("Select a demo below.")


# Object notation
st.sidebar.header("This is the header in the sidebar")


# "with" notation
with st.sidebar:
    st.header("This is the header")
    st.subheader("This is the subheading")
    st.write(10+20)
st.header("Hello")


# Columns

col1, col2 = st.columns(2)
with col1:
    st.text("Welcome")
    st.subheader("Coding101withsteve")


with col2:
    st.text("Not welcome")


#  Clickable images


clicked = clickable_images(
    [
        "https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=700",
        "https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=700",
        "https://images.unsplash.com/photo-1582550945154-66ea8fff25e1?w=700",
        "https://images.unsplash.com/photo-1591797442444-039f23ddcc14?w=700",
        "https://images.unsplash.com/photo-1518727818782-ed5341dbd476?w=700",
    ],
    titles=[f"Image #{str(i)}" for i in range(5)],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "200px"},
)

st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

# Metric

import streamlit as st

st.metric(label="Gas price", value=4, delta=-0.5,
    delta_color="inverse")

st.metric(label="Active developers", value=123, delta=123,
    delta_color="off")
